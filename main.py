# from PySide6 import QtWidgets
# import numpy as np
# from pyqtgraph.Qt import QtGui, QtCore, QtWidgets
from pyqtgraph.Qt import mkQApp
# import pyqtgraph as pg

import struct
import pyaudio
# from scipy.fftpack import fft

import sys
# import time
# from kaudio.audio import AudioListener
from kaudio.controller import Controller
import argparse

import time




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
def list_all_audio_devices():
    pa = pyaudio.PyAudio()
    for id in range(pa.get_device_count()):
        dev_dict = pa.get_device_info_by_index(id)
        for key, value in dev_dict.items():
            print(key, value)
        print('\n')




if __name__ == '__main__':
    args = parse_args()
        
    if args.list_devices:
        list_all_audio_devices()
    else:

        # app = QtWidgets.QApplication(sys.argv)
        # app = QtWidgets.QApplication([])
        app = mkQApp()
        controller = Controller()
        # controller.start()
        sys.exit(app.exec_())
