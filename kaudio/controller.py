# import numpy as np
# from PySide6 import QtWidgets, QtCore
from pyqtgraph.Qt import QtWidgets, QtCore, QtGui


from kaudio.plots import KaStereoWaveform
from kaudio.audio import AudioListener



# import struct
# import pyaudio
# from scipy.fftpack import fft

# import sys
# import time

# import pretty_errors

class Controller(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        # self.view = View()
        self.setCentralWidget(View())
        self.setWindowTitle('KAudio')

        dock = QtWidgets.QDockWidget("Options", parent=self)
        dock.setFeatures(dock.NoDockWidgetFeatures)

        

        self.btn_rcd_on = QtWidgets.QPushButton("Start listening", dock)
        # self.layout.addWidget(self.btn_rcd_on)
        self.btn_rcd_off = QtWidgets.QPushButton("Stop listening", dock)
        # self.layout.addWidget(self.btn_rcd_off)
        
        self.btn_rcd_on.clicked.connect(self.record_on)
        # self.btn_rcd_on.show()
        
        
        
        self.btn_rcd_off.clicked.connect(self.record_off)
        self.btn_rcd_off.hide()
        dock.setWidget(self.btn_rcd_off)
        dock.setWidget(self.btn_rcd_on)
        self.addDockWidget(
            QtGui.Qt.RightDockWidgetArea,
            dock,
        )
        
        # def set_plotdata(self, name, data_x, data_y):
        # if name in self.traces:
        #     self.traces[name].setData(data_x, data_y)
        # else:
        #     if name == 'waveform':
        #         self.traces[name] = self.waveform.plot(pen='c', width=3)
        #         self.waveform.setYRange(-1, 1, padding=0)
        #         self.waveform.setXRange(0, 2 * self.CHUNK, padding=0.005)
        #     if name == 'spectrum':
        #         self.traces[name] = self.spectrum.plot(pen='m', width=3)
        #         self.spectrum.setLogMode(x=True, y=True)
        #         self.spectrum.setYRange(-4, 0, padding=0)
        #         self.spectrum.setXRange(
        #             np.log10(20), np.log10(self.RATE / 2), padding=0.005)
        
        
        # btn_quit = QtWidgets.QPushButton('Force Quit', self)
        # btn_quit.clicked.connect(QtWidgets.QApplication.instance().quit)
        # btn_quit.resize(btn_quit.sizeHint())
        # btn_quit.move(90, 100)
        
        # sp_xlabels = [
        #     (np.log10(10), '10'), (np.log10(100), '100'),
        #     (np.log10(1000), '1000'), (np.log10(22050), '22050')
        # ]
        # sp_xaxis = pg.AxisItem(orientation='bottom')
        # sp_xaxis.setTicks([sp_xlabels])

        # self.waveform = 1
        # self.spectrum = self.win.addPlot(
        #     title='SPECTRUM', row=2, col=1, axisItems={'bottom': sp_xaxis},
        # )
        self.show()

    def record_on(self):
        self.audio_listener = AudioListener()

        # self.timer_update.start(20)
        self.timer_update.start(1000)


        if not hasattr(self, 'stereo_waveforms'):
            self.stereo_waveforms = KaStereoWaveform()
            self.layout.addWidget(self.stereo_waveforms)
        self.stereo_waveforms.hide()
        
        # print('hiding record on')
        self.btn_rcd_on.hide()
        self.btn_rcd_off.show()
        # print('finishing hiding record on')
    def record_off(self):
        self.audio_listener.stream.stop_stream()
        self.btn_rcd_off.hide()
        self.btn_rcd_on.show()
        
    def update(self):
        '''
        Main update loop
        '''
        pass
        # x, frame = self.audio_listener.get_update()

        # if hasattr(self, "work") and callable(self.work):
        #     self.stereo_waveforms.update(x, frame)
class View(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QtWidgets.QVBoxLayout(self)

        self.timer_update = QtCore.QTimer()
        self.timer_update.timeout.connect(self.update)

    