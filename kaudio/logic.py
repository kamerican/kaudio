from pathlib import Path
import itertools
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
        mix.export(filename, format="mp3")
    def get_vocals(self, filename):
        song_path = self.song_dir / filename
        inst_path = self.inst_dir / filename

        # song = AudioSegment.from_file(file=song_path, format=song_path.suffix[1:])
        # inst = AudioSegment.from_file(file=inst_path, format=inst_path.suffix[1:])

        song = numpy.array([0, 0, 0, 1, 2, 3, 4, 5, 4, 3, 2, 1, 0, 0, 0, 0, 0, 0])
        inst = numpy.array([0, 0, 0, 0, 0, 0, 1, 2, 3, 4, 5, 4, 3, 2, 1, 0, 0, 0])

        # inst = inst.invert_phase()
        y2 = song
        y1 = inst

        print("convolving...")
        y3 = signal.correlate(y2, y1)
        dt = numpy.arange(1-len(y1), len(y1))
        print(dt[y3.argmax()])

        A = fftpack.fft(y1)
        B = fftpack.fft(y2)
        Ar = A.conjugate()
        y4 = fftpack.ifft(Ar*B)

        print(numpy.argmax(y4))

        print("finished convolving...")
        print("lengths:", len(y1), len(y2), len(y3), len(y4))

        fig, ax_array = plt.subplots(4, 1)
        ax1, ax2, ax3, ax4 = ax_array.flatten()




        ax1.plot(y1)
        ax2.plot(y2)
        ax3.plot(y3)
        ax4.plot(y4)
        ax1.plot(y2[y4.argmax():])

        fig.tight_layout()
        # fig.savefig('test.png')
        plt.show()
        