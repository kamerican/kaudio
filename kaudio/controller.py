# import sys
# import time
from pathlib import Path
working_dir = Path('e:/data/kaudio')
test_file = working_dir / '5 Luda.mp4.aac'
# test_file = working_dir / 'HELLO UJUNG EP3.wav'
# test_file = working_dir / "07. Don't Touch.flac"



from pyqtgraph.Qt import QtWidgets, QtCore, QtGui
# import pyqtgraph as pg

from kaudio.view import View
from kaudio.audio import AudioFile, AudioPlayer



# import struct
# import pyaudio
# from scipy.fftpack import fft





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


        # self.btn_load_audio_file = QtWidgets.QPushButton("Load audio file", dock)
        # self.btn_unload_audio_file = QtWidgets.QPushButton("Unload audio file", dock)
        # self.btn_load_audio_file.clicked.connect(self.load_audio_file)
        # self.btn_unload_audio_file.clicked.connect(self.unload_audio_file)
        # self.btn_unload_audio_file.hide()
        # dock_layout.addWidget(self.btn_load_audio_file)
        # dock_layout.addWidget(self.btn_unload_audio_file)

        
        self.chkbx_load_audio_file = QtWidgets.QCheckBox("Load audio file", dock)
        self.chkbx_load_audio_file.stateChanged.connect(self.load_audio_file)
        dock_layout.addWidget(self.chkbx_load_audio_file)

        self.chkbx_load_audio_player = QtWidgets.QCheckBox("Load audio player", dock)
        self.chkbx_load_audio_player.stateChanged.connect(self.load_audio_player)
        self.chkbx_load_audio_player.hide()
        dock_layout.addWidget(self.chkbx_load_audio_player)
        
        self.chkbx_start_playback = QtWidgets.QCheckBox("Playback audio", dock)
        self.chkbx_start_playback.stateChanged.connect(self.playback_audio)
        self.chkbx_start_playback.hide()
        dock_layout.addWidget(self.chkbx_start_playback)

        # self.timer_update = QtCore.QTimer()
        # self.timer_update.timeout.connect(self.update)

        dock.setWidget(self.widget_options)
        self.addDockWidget(
            QtGui.Qt.RightDockWidgetArea,
            dock,
        )
        self.show()
    @QtCore.Slot()
    def load_audio_file(self):
        if self.chkbx_load_audio_file.isChecked():
            self.audio_listener = AudioFile(test_file)
            self.chkbx_load_audio_player.show()
        else:
            self.chkbx_load_audio_player.setChecked(False)
            self.chkbx_load_audio_player.hide()
    @QtCore.Slot()
    def load_audio_player(self):
        if self.chkbx_load_audio_player.isChecked():
            self.audio_player = AudioPlayer(self.audio_listener.audio_segment, 1)
            self.chkbx_start_playback.show()
        else:
            self.audio_player.unload()
            self.chkbx_start_playback.setChecked(False)
            self.chkbx_start_playback.hide()
    @QtCore.Slot()
    def playback_audio(self):
        if self.chkbx_start_playback.isChecked():
            self.audio_player.play()
            print('Started playback.')
        else:
            self.audio_player.stop()
            print('Stopped playback.')
    # @QtCore.Slot()
    # def (self):
        
    # @QtCore.Slot()
    # def (self):
            
        # self.timer_update.stop()
        # self.timer_update.start(150)
        # self.timer_update.start(500)

        # if not 'stereo_waveform' in self.plots:
        #     self.plots['stereo_waveform'] = KaStereoWaveform()
        #     self.view.add_widget(self.plots['stereo_waveform'])
        #     self.chkbx_load_audio.setChecked(True)
        #     self.chkbx_load_audio.show()
        #     # self.button = QtWidgets.QPushButton("Hide waveforms")
        # if not hasattr(self, 'stereo_waveforms'):
        #     self.stereo_waveforms = KaStereoWaveform()
        #     self.layout.addWidget(self.stereo_waveforms)
        # self.stereo_waveforms.hide()
        
        # print('hiding record on')
        # self.btn_start_playback.hide()
        # self.btn_stop_playback.show()
        # print('finishing hiding record on')


        





    # def update(self):
    #     '''
    #     Main update loop
    #     '''
    #     # pass
    #     x, frame = self.audio_listener.get_update()

    #     if 'stereo_waveform' in self.plots and self.plots['stereo_waveform'].update_flag:
    #         self.plots['stereo_waveform'].update(x, frame)



    