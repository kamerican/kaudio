import pyqtgraph as pg

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
