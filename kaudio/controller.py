# import numpy as np
# from PySide6 import QtWidgets, QtCore
from pyqtgraph.Qt import QtWidgets, QtCore, QtGui
import pyqtgraph as pg

from kaudio.plots import KaStereoWaveform, View
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
        self.view = View()
        self.setCentralWidget(self.view)
        self.setWindowTitle('KAudio')
        self.resize(800, 600)

        self.plots = dict()


        dock = QtWidgets.QDockWidget("Options", self)
        dock.setFeatures(dock.NoDockWidgetFeatures)
        
        self.widget_options = QtWidgets.QWidget(dock)
        dock_layout = QtWidgets.QVBoxLayout(self.widget_options)




        self.btn_rcd_on = QtWidgets.QPushButton("Start listening", dock)
        self.btn_rcd_off = QtWidgets.QPushButton("Stop listening", dock)
        self.btn_rcd_on.clicked.connect(self.record_on)
        self.btn_rcd_off.clicked.connect(self.record_off)
        self.btn_rcd_off.hide()
        dock_layout.addWidget(self.btn_rcd_off)
        dock_layout.addWidget(self.btn_rcd_on)
        
        self.chkbx_stereo_waveform = QtWidgets.QCheckBox("Show waveform", dock)
        # self.chkbx_stereo_waveform.
        self.chkbx_stereo_waveform.stateChanged.connect(self.display_waveform)
        self.chkbx_stereo_waveform.hide()
        dock_layout.addWidget(self.chkbx_stereo_waveform)
        dock.setWidget(self.widget_options)
        

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
        
        self.timer_update = QtCore.QTimer()
        self.timer_update.timeout.connect(self.update)

        self.show()
    @QtCore.Slot()
    def record_on(self):
        self.audio_listener = AudioListener()

        self.timer_update.start(150)
        # self.timer_update.start(500)

        if not 'stereo_waveform' in self.plots:
            self.plots['stereo_waveform'] = KaStereoWaveform()
            self.view.add_widget(self.plots['stereo_waveform'])
            self.chkbx_stereo_waveform.setChecked(True)
            self.chkbx_stereo_waveform.show()
            # self.button = QtWidgets.QPushButton("Hide waveforms")
        # if not hasattr(self, 'stereo_waveforms'):
        #     self.stereo_waveforms = KaStereoWaveform()
        #     self.layout.addWidget(self.stereo_waveforms)
        # self.stereo_waveforms.hide()
        
        # print('hiding record on')
        self.btn_rcd_on.hide()
        self.btn_rcd_off.show()
        # print('finishing hiding record on')
    @QtCore.Slot()
    def record_off(self):
        self.audio_listener.stream.stop_stream()
        self.btn_rcd_off.hide()
        self.btn_rcd_on.show()
        self.timer_update.stop()
    @QtCore.Slot()
    def display_waveform(self):
        if self.chkbx_stereo_waveform.isChecked():
            self.plots['stereo_waveform'].show()
            self.plots['stereo_waveform'].update_flag = True
        else:
            self.plots['stereo_waveform'].hide()
            self.plots['stereo_waveform'].update_flag = False
    def update(self):
        '''
        Main update loop
        '''
        # pass
        x, frame = self.audio_listener.get_update()

        if 'stereo_waveform' in self.plots and self.plots['stereo_waveform'].update_flag:
            self.plots['stereo_waveform'].update(x, frame)



    