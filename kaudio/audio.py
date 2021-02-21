import numpy as np
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg

import struct
import pyaudio
from scipy.fftpack import fft

import sys
import time

# import pretty_errors

class AudioListener(object):
    def __init__(self):

        # pyaudio stuff
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 2
        self.RATE = 48000
        self.CHUNK = 7168
        
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
            input_device_index=3,
            output=True,
            output_device_index=8,
            frames_per_buffer=self.CHUNK,
        )
        # self.x = np.arange(0, 2 * self.CHUNK, 2)
        self.x = np.arange(0, self.CHUNK, 1)
        # self.f = np.linspace(0, self.RATE / 2, int(self.CHUNK / 2))

    def get_update(self):
        frame = self.get_frame()
        return self.x, frame

    def get_frame(self):
        # frame = np.frombuffer(self.stream.read(self.CHUNK), dtype=np.int16)/2**15
        frame = np.frombuffer(self.stream.read(self.CHUNK), dtype=np.int16)
        # print(frame.shape)
        frame = np.stack((frame[::2], frame[1::2]), axis=0)  # channels on separate axes
        # print(frame.shape)
        return frame

        # # sp_data = fft(np.array(frame[0], dtype='int8') - 128)

        # sp_data = fft(frame[0])
        # sp_data = np.abs(sp_data[0:int(self.CHUNK / 2)]) * 2 / (128 * self.CHUNK)

        # # sp_data = np.abs(sp_data[0:int(self.CHUNK / 2)]) * 2 / (128 * self.CHUNK)


        # self.set_plotdata(name='spectrum', data_x=self.f, data_y=sp_data)
