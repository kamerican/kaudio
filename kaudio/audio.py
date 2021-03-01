import time
from pathlib import Path

import numpy as np
from pydub import AudioSegment
import pyaudio

from kaudio.util import get_pyaudio_device_indices

class AudioPlayer(object):
    """
    Reads audio files for further processing and playback.
    """
    def __init__(self, audio_segment: AudioSegment, chunk_seconds):
        self.pa = pyaudio.PyAudio()
        # print(self.pa.get_default_output_device_info())
        # print(self.pa.get_host_api_info_by_index(4))
        devices = get_pyaudio_device_indices(
            self.pa,
            pyaudio.paWASAPI,
            output_device_name='VoiceMeeter VAIO3 Input (VB-Audio VoiceMeeter VAIO3)',
        )
        # self.FORMAT = pyaudio.paInt16
        # self.CHANNELS = 2
        # self.RATE = 48000
        # self.CHUNK = self.RATE/10
        
        self.chunk_ms = chunk_seconds*1000
        self.slice_generator = audio_segment[::self.chunk_ms]
        chunk = chunk_seconds*audio_segment.frame_rate
        
        
        
        # print(audio_segment.channels)
        # print(devices)
        # print(devices['output'])
        self.stream = self.pa.open(
            format=self.pa.get_format_from_width(audio_segment.sample_width),
            channels=audio_segment.channels,
            rate=audio_segment.frame_rate,
            output=True,
            # output_device_index=26,
            output_device_index=devices['output'],
            frames_per_buffer=chunk,
            stream_callback=self.callback_read,
        )
        self.stream.stop_stream()
    def callback_read(self, in_data, frame_count, time_info, status_flags):
        """
        Nonblocking callback stream read.
        ---
        Notes from PyAudio documentation:
        stream_callback –
            Specifies a callback function for non-blocking (callback) operation. Default is None, which indicates blocking operation (i.e., Stream.read() and Stream.write()). To use non-blocking operation, specify a callback that conforms to the following signature:

            callback(in_data,     # recorded data if input=True; else None
                    frame_count,  # number of frames
                    time_info,    # dictionary
                    status_flags) # PaCallbackFlags
            time_info is a dictionary with the following keys: input_buffer_adc_time, current_time, and output_buffer_dac_time; see the PortAudio documentation for their meanings. status_flags is one of PortAutio Callback Flag.

            The callback must return a tuple:

            (out_data, flag)
            out_data is a byte array whose length should be the (frame_count * channels * bytes-per-channel) if output=True or None if output=False. flag must be either paContinue, paComplete or paAbort (one of PortAudio Callback Return Code). When output=True and out_data does not contain at least frame_count frames, paComplete is assumed for flag.

            Note: stream_callback is called in a separate thread (from the main thread). Exceptions that occur in the stream_callback will:

            print a traceback on standard error to aid debugging,
            queue the exception to be thrown (at some point) in the main thread, and
            return paAbort to PortAudio to stop the stream.
            Note: Do not call Stream.read() or Stream.write() if using non-blocking operation.

            See: PortAudio’s callback signature for additional details: http://portaudio.com/docs/v19-doxydocs/portaudio_8h.html#a8a60fb2a5ec9cbade3f54a9c978e2710

            Raises:	
            ValueError – Neither input nor output are set True.
        """
        out_data = next(self.slice_generator).raw_data
        print("Finished writing {} frames".format(frame_count))
        # time.sleep(1)

        return out_data, pyaudio.paContinue
    def play(self):
        """
        Starts the pyaudio stream to do things in the callback function on a audio segment.
        """
        self.stream.start_stream()
    def stop(self):
        """
        Ends the stream and closes pyaudio.
        """
        self.stream.stop_stream()
    def unload(self):
        """
        Closes the stream and PyAudio
        """
        if self.stream.is_active():
            self.stream.stop_stream()
        self.stream.close()
        self.pa.terminate()
class AudioFile(object):
    """
    Uses AudioSegment to process audio samples.
    """
    def __init__(self, path: Path):
        print("Loading: {}".format(path.name))
        time_start = time.time()
        self.audio_segment = AudioSegment.from_file(path, path.suffix[1:])
        print("Finished loading in {}".format(time.time() - time_start))
        print("Sample rate: {}".format(self.audio_segment.frame_rate))
        print("Format: {}-bit".format(self.audio_segment.sample_width * 8))
        print("Number of channels: {}".format(self.audio_segment.channels))

        if self.audio_segment.frame_rate == 44100:
            print("Changing frame rate from 44100Hz to 48000Hz.")
            self.audio_segment = self.audio_segment.set_frame_rate(48000)

        if self.audio_segment.channels == 1:
            samples = self.audio_segment.get_array_of_samples()
            self.samples = np.array(samples, dtype=np.float32)/np.iinfo(samples.typecode).max
            print("\nSample shape: {}".format(self.samples.shape))
            print("Number of samples: {}".format(self.samples.shape[0]))
            self.time_domain = np.arange(0, self.samples.shape[0])/self.audio_segment.frame_rate
            # view.add_trace(0, 0, x[:441000], samples[:441000], (0, 10), (-1, 1), "Mono Channel")
        elif self.audio_segment.channels == 2:
            stereo_segments = self.audio_segment.split_to_mono()
            samples = [s.get_array_of_samples() for s in stereo_segments]
            
            self.samples = np.array(samples, dtype=np.float32)/np.iinfo(samples[0].typecode).max
            print("\nSample shape: {}".format(self.samples.shape))
            print("Number of samples: {}".format(self.samples.shape[1]))
            self.time_domain = np.arange(0, self.samples.shape[1])/self.audio_segment.frame_rate
            # view.add_trace(0, 0, x[:441000], samples[0], (0, np.max(x)), (-1, 1), "Left Channel")
            # view.add_trace(0, 0, x[:441000], samples[0][:441000], (0, 10), (-1, 1), "Left Channel")
            # view.add_trace(1, 0, x[:441000], samples[0], (0, np.max(x)), (-1, 1), "Right Channel")
            # view.add_trace(1, 0, x[:441000], samples[1][:441000], (0, 10), (-1, 1), "Right Channel")
        else:
            raise ValueError("Too many channels!")
        