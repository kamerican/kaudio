from pyqtgraph.Qt import QtWidgets, QtCore
import pyqtgraph as pg
pg.setConfigOptions(antialias=True)
import numpy as np
# import pretty_errors


class View(QtWidgets.QWidget):
# class GraphicsView(pg.GraphicsLayoutWidget):
    def __init__(self):
        super().__init__()
        self.layout = QtWidgets.QVBoxLayout(self)
    def add_widget(self, widget):
        self.layout.addWidget(widget)



class KaStereoWaveform(pg.GraphicsLayoutWidget):
    def __init__(self):
        super().__init__()
        self.update_flag = True
        # self.stereo_waveforms = pg.GraphicsLayoutWidget(show=True)
        # self.stereo_waveforms.setWindowTitle('pyqtgraph example: Scrolling Plots')
        # self.setGeometry(5, 115, 1910, 1070)


        
        # self.add_waveform_plot("Stereo Left", 0, 0)
        # self.add_waveform_plot("Stereo Right", 1, 0)

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
        self.left_channel_plotitem = self.addPlot(
            title="Left Channel",
            row=0,
            col=0,
            # axisItems={
            #     'bottom': x_axis,
            #     'left': y_axis
            # },
        )
        self.right_channel_plotitem = self.addPlot(
            title="Right Channel",
            row=0,
            col=1,
            # axisItems={
            #     'bottom': x_axis,
            #     'left': y_axis
            # },
        )

        self.left_channel_plotitem.setXRange(0, 7168, padding=0.005)
        self.left_channel_plotitem.setYRange(-1, 1, padding=0)
        self.left_channel_plotdataitem = self.left_channel_plotitem.plot(
            # np.arange(0, 9, 2, dtype=np.int16),
            pen='c',
            width=3,
        )
        
        self.right_channel_plotitem.setXRange(0, 7168, padding=0.005)
        self.right_channel_plotitem.setYRange(-1, 1, padding=0)
        self.right_channel_plotdataitem = self.right_channel_plotitem.plot(
            # np.arange(0, 9, 2),
            pen='c',
            width=3,
        )

    def update(self, x, frame):
        # print(frame.shape)
        left = frame[0]/2**15
        right = frame[1]/2**15
        # print(x.shape)
        # print(left.shape)
        # print(type(left))
        # print(right.shape)
        # print(type(right))
        # print(type(self.left_channel_plotdataitem))
        # print(type(self.right_channel_plotdataitem))
        # print(self.left_channel.listDataItems())
        # print(self.right_channel.listDataItems())
        # print(self.left_channel.setData)

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
