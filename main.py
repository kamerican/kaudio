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
# import pretty_errors

# class Controller(object):
#     def __init__(self):
        
        
#         self.main_gui = MainGui()
#         # self.timer = QtCore.QTimer()
#         # self.timer.timeout.connect(self.update)


#     def start(self):
#         # Start timer which reactivates every 20 ms
#         self.timer.start(20)
#         # self.timer.start(4000)

#     def update(self):
        
#         # print(5)
        
#         # print(6)
#         self.main_gui.update(x, frame)
#         # print(7)
if __name__ == '__main__':
    # app = QtWidgets.QApplication(sys.argv)
    # app = QtWidgets.QApplication([])
    app = mkQApp()
    controller = Controller()
    # controller.start()
    sys.exit(app.exec_())
