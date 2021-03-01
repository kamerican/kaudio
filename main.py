import sys
import argparse

from pyqtgraph.Qt import mkQApp

from kaudio.util import list_all_audio_devices
from kaudio.controller import Controller

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
        controller = Controller()
        sys.exit(app.exec_())

        

        
