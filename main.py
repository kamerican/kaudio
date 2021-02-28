import sys
import argparse
import time
from pathlib import Path

import numpy as np
# from scipy.fftpack import fft

import pyqtgraph as pg
from pyqtgraph.Qt import mkQApp, QtGui, QtCore, QtWidgets

from pydub import AudioSegment
from pydub.playback import play
import pyaudio


# import time
from kaudio.util import list_all_audio_devices, get_pyaudio_device_indices
# from kaudio.controller import Controller


working_dir = Path('e:/data/kaudio')
# test_file = working_dir / '5 Luda.mp4.aac'
# test_file = working_dir / 'HELLO UJUNG EP3.wav'
test_file = working_dir / "07. Don't Touch.flac"



class View(pg.GraphicsLayoutWidget):
    def __init__(self):
        super().__init__()
        self.update_flag = True
        self.setWindowTitle("Graphics Testing")
        self.resize(800, 600)

        self.traces = list()
        
        
    def add_trace(self, row, col, x, y, x_range, y_range, name):
        """
        Add a trace to the view.
        """
        # x_axis = pg.AxisItem(orientation='bottom')
        # x_axis.setTicks([
        #     (0, '0'),
        #     (2048, '2048'),
        #     (4096, '4096'),
        # ])
        # y_axis = pg.AxisItem(orientation='left')
        # y_axis.setTicks([
        #     (-1, '-1'),
        #     (0, '0'),
        #     (1, '1'),
        # ])
        plot_item = self.addPlot(
            title=name,
            row=row,
            col=col,
            # axisItems={
            #     'bottom': x_axis,
            #     'left': y_axis
            # },
        )
        plot_item.setXRange(x_range[0], x_range[1], padding=0)
        plot_item.setYRange(y_range[0], y_range[1], padding=0)
        data_item = plot_item.plot(
            x,
            y,
            pen='c',
            width=3,
        )
        self.traces.append({
            'plot': plot_item,
            'data': data_item,
        })
    def update(self, x, frame):
        # print(frame.shape)
        left = frame[0]/2**15
        right = frame[1]/2**15

        self.left_channel_plotdataitem.setData(
            # x[:10],
            # left[:10],
            x=x,
            y=left,
        )

        self.right_channel_plotdataitem.setData(
            # x[:10],
            # right[:10],
            x=x,
            y=right,
        )

        # self.left_channel.setData(
        #     x[:10],
        #     left[:10],
        #     # x=x[:10],
        #     # y=left[:10],
        # )
    
        # self.right_channel.setData(
        #     x[:10],
        #     right[:10],
        #     # x=x[:10],
        #     # y=right[:10],
        # )
        # # sp_data = fft(np.array(frame[0], dtype='int8') - 128)
        # sp_data = fft(frame[0])
        # sp_data = np.abs(sp_data[0:int(self.CHUNK / 2)]) * 2 / (128 * self.CHUNK)
        # # sp_data = np.abs(sp_data[0:int(self.CHUNK / 2)]) * 2 / (128 * self.CHUNK)
        # self.set_plotdata(name='spectrum', data_x=self.f, data_y=sp_data)

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
        # print(type(devices['output'][0]))
        # print(devices['output'][0])
        self.stream = self.pa.open(
            format=self.pa.get_format_from_width(audio_segment.sample_width),
            channels=audio_segment.channels,
            rate=audio_segment.frame_rate,
            output=True,
            # output_device_index=26,
            output_device_index=devices['output'][0],
            # output_device_index=devices['output'],
            frames_per_buffer=chunk,
            stream_callback=self.callback_read,
        )
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

        return out_data, pyaudio.paContinue
    def play(self):
        """
        Starts the pyaudio stream to do things in the callback function on a audio segment.
        """
        pass
    def stop(self):
        """
        Ends the stream and closes pyaudio.
        """
        self.stream.stop_stream()
        self.stream.close()
        self.pa.terminate()


def get_pyaudio_device_indices(pa, API, input_device_name=None, output_device_name=None):
    """
    Returns a dict as:
    device['input'] = input device index
    device['output'] = output device index
    """
    host_api_dict = pa.get_host_api_info_by_type(API)
    input_device = None
    output_device = None
    
    if input_device_name:
        print("Input device: {}".format(input_device_name))
    if output_device_name:
        print("Output device: {}".format(output_device_name))
    
    
    for device_index in range(host_api_dict['deviceCount']):
        device_dict = pa.get_device_info_by_host_api_device_index(
            host_api_dict['index'],
            device_index,
        )
        if device_dict['name'] == input_device_name:
            input_device = device_dict.copy()
            print("Found specified input device (index={})".format(
                input_device['index']
            ))
        elif device_dict['name'] == output_device_name:
            output_device = device_dict.copy()
            print("Found specified output device (index={})".format(
                output_device['index']
            ))
    
    devices = dict()
    if input_device_name:
        devices['input'] = input_device['index'],
    if output_device_name:
        devices['output'] = output_device['index'],
    
    return devices

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--list-devices', action='store_true')
    
    
    # parser.add_argument('--device', type=int, default=None, dest='device',
    #                     help='pyaudio (portaudio) device index')
    # parser.add_argument('--height', type=int, default=450, dest='height',
    #                     help='height, in pixels, of the visualizer window')
    # parser.add_argument('--n_frequency_bins', type=int, default=400, dest='frequency_bins',
    #                     help='The FFT features are grouped in bins')
    # parser.add_argument('--verbose', action='store_true')
    # parser.add_argument('--window_ratio', default='24/9', dest='window_ratio',
    #                     help='float ratio of the visualizer window. e.g. 24/9')
    # parser.add_argument('--sleep_between_frames', dest='sleep_between_frames', action='store_true',
    #                     help='when true process sleeps between frames to reduce CPU usage (recommended for low update rates)')
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
        
    if args.list_devices:
        list_all_audio_devices()
    else:
        # app = QtWidgets.QApplication(sys.argv)
        # app = QtWidgets.QApplication([])
        app = mkQApp()
        view = View()
        view.show()

        

        test_segment = AudioSegment.from_file(test_file, test_file.suffix[1:])
        print("Sample rate: {}".format(test_segment.frame_rate))
        print("Number of bits: {}-bit".format(test_segment.sample_width * 8))
        print("Number of channels: {}".format(test_segment.channels))
        
        if test_segment.channels == 1:
            samples = test_segment.get_array_of_samples()
            samples = np.array(samples, dtype=np.float32)/np.iinfo(samples.typecode).max
            print(samples.shape)
            x = np.arange(0, samples.shape[0])/test_segment.frame_rate
            view.add_trace(0, 0, x[:441000], samples[:441000], (0, 10), (-1, 1), "Mono Channel")
        elif test_segment.channels == 2:
            stereo_segments = test_segment.split_to_mono()
            samples = [s.get_array_of_samples() for s in stereo_segments]
            
            samples = np.array(samples, dtype=np.float32)/np.iinfo(samples[0].typecode).max
            print(samples.shape)
            print(samples[0].shape)
            print(samples[1].shape)
            x = np.arange(0, samples.shape[1])/test_segment.frame_rate
            # view.add_trace(0, 0, x[:441000], samples[0], (0, np.max(x)), (-1, 1), "Left Channel")
            view.add_trace(0, 0, x[:441000], samples[0][:441000], (0, 10), (-1, 1), "Left Channel")
            # view.add_trace(1, 0, x[:441000], samples[0], (0, np.max(x)), (-1, 1), "Right Channel")
            view.add_trace(1, 0, x[:441000], samples[1][:441000], (0, 10), (-1, 1), "Right Channel")

        else:
            raise ValueError("Too many channels!")
        
        

        
        ap = AudioPlayer(test_segment, 5)

        # ap.play()
        ap.stream.start_stream()


        while ap.stream.is_active():
            time.sleep(1)

        
        print('finished playing')
        ap.stop()
        
        sys.exit(app.exec_())

        

        
