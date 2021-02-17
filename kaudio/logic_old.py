from pathlib import Path
import itertools
import time
import array
import numpy
from scipy import signal, fftpack
import matplotlib.pyplot as plt
from pydub import AudioSegment

class Song():
    """
    Class managing processes on songs
    """
    def __init__(self, filepath):
        self.filepath = filepath
        self.audio = AudioSegment.from_file(
            file=filepath,
            format=filepath.suffix[1:],
        )
        self.array = numpy.array(self.audio.get_array_of_samples())



class Manager():
    """
    Class managing songs.
    """
    def __init__(self):
        base_dir = Path(__file__).parent
        self.song_dir = base_dir / 'song'
        self.inst_dir = base_dir / 'inst'
        self.vocal_dir = base_dir / 'vocal'
        self.file_extension_list = ['*.mp3', '*.m4a']
    def get_song_gen(self, directory):
        """
        Returns generator containing songs from a given directory.
        """
        glob_gen_list = []
        for pattern in self.file_extension_list:
            glob_gen = directory.glob(pattern)
            glob_gen_list.append(glob_gen)
        return itertools.chain.from_iterable(glob_gen_list)
    def overlay_invert_mono_from_stereo(self, filename):
        """
        Split stereo into two mono tracks, invert one and mix them together.
        """ 
        song = Song(self.song_dir / filename)
        split = song.audio.split_to_mono()
        left_channel = split[0]
        right_channel = split[1]
        mix = left_channel.overlay(right_channel.invert_phase())
        mix.export(filename, format='mp3')
    def get_all_vocals(self):
        file_gen = self.get_song_gen(self.song_dir)
        export_extension = 'mp3'
        for f in file_gen:
            destination_path = self.vocal_dir / "{0}.{1}".format(
                f.stem,
                export_extension,
            )
            if not destination_path.is_file():
                print("Processing:", f.name)
                to_export = self.get_vocals(f.name)                
                to_export.export(
                    destination_path,
                    format=export_extension,
                )
    def get_vocals(self, filename):
        song_path = self.song_dir / filename
        inst_path = self.inst_dir / filename

        song = AudioSegment.from_file(file=song_path, format=song_path.suffix[1:])
        inst = AudioSegment.from_file(file=inst_path, format=inst_path.suffix[1:])
        full_song_array = song.get_array_of_samples()
        full_inst_array = inst.get_array_of_samples()
        song_array = full_song_array[:5000000]
        inst_array = full_inst_array[:5000000]
        n = len(song_array)
        shift = self.get_shift(song_array, inst_array)
        if shift < n/2:
            print("Modifying inst")
            full_inst_array = full_inst_array[shift:]
            inst_shifted = inst._spawn(full_inst_array)
            to_export = song.overlay(inst_shifted.invert_phase())
        else:
            print("Modifying song")
            full_song_array = full_song_array[n - shift:]
            song_shifted = song._spawn(full_song_array)
            to_export = inst.overlay(song_shifted.invert_phase())
        return to_export
        
        
    def get_shift(self, y1, y2):
        y1 = numpy.array(y1)
        y2 = numpy.array(y2)
        y1 = y1 - y1.mean()
        y1 = y1 / y1.std()
        y2 = y2 - y2.mean()
        y2 = y2 / y2.std()

        now = time.time()
        A = fftpack.fft(y1)
        B = fftpack.fft(y2)
        Ar = A.conjugate()
        y3 = fftpack.ifft(Ar*B)
        print("FFT time:", time.time() - now)

        return y3.argmax()
    # def correlate_method(self, y1, y2):
    #     now = time.time()
    #     y3 = signal.correlate(y2, y1)
    #     print("Correlate time:", time.time() - now)

    #     dt = numpy.arange(1-len(y1), len(y1))
    #     print(dt[y3.argmax()])


    # fig, ax_array = plt.subplots(3, 1)
    # ax1, ax2, ax3 = ax_array.flatten()
    # ax1.plot(y1)
    # ax2.plot(y2)
    # ax3.plot(y3)
    # if shift < len(y1)/2:
    #     ax1.plot(y2[shift:])
    # else:
    #     ax2.plot(y1[len(y1) - shift:])

    # fig.tight_layout()
    # # fig.savefig('test.png')
    # plt.show()
