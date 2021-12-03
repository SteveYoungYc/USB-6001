import sys

import numpy as np
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (QWidget, QToolTip,
                             QPushButton, QApplication, QMainWindow)
from PyQt5.QtGui import QFont

import pyqtgraph as pg
from USB import USB
from MainWindow import Ui_MainWindow


class MyGraphWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MyGraphWindow, self).__init__()
        self.setupUi(self)  # 初始化窗口
        self.p2 = self.set_graph_ui()  # 设置绘图窗口

        self.originPos = 0
        self.data1 = np.zeros(100)
        self.curve1 = self.p2.plot(self.data1)
        self.curve1.setData(self.data1)
        # 设定定时器
        self.timer = pg.QtCore.QTimer()
        # 定时器信号绑定 update_data 函数
        self.timer.timeout.connect(self.update_data)
        # 定时器间隔50ms，可以理解为 50ms 刷新一次数据
        self.timer.start(100)

    def set_graph_ui(self):
        pg.setConfigOptions(antialias=True)  # pg全局变量设置函数，antialias=True开启曲线抗锯齿

        win = pg.GraphicsLayoutWidget()  # 创建pg layout，可实现数据界面布局自动管理

        # pg绘图窗口可以作为一个widget添加到GUI中的graph_layout，当然也可以添加到Qt其他所有的容器中
        self.graph_layout.addWidget(win)
        win.nextRow()  # layout换行，采用垂直排列，不添加此行则默认水平排列
        p2 = win.addPlot(title="USB DATA")
        p2.setLabel('left', text='voltage', color='#ffffff')
        p2.showGrid(x=True, y=True)
        p2.setLogMode(x=False, y=False)
        p2.setLabel('bottom', text='time', units='s')
        # p2.addLegend()

        return p2

    def plot(self, x, y):
        self.p2.plot(x, y, pen='g', name='sin(x)', clear=True)

    def update_data(self):
        self.data1[:-1] = self.data1[1:]
        self.data1[-1] = 1
        self.originPos += 1
        self.curve1.setPos(self.originPos, 0)
        # 数据填充到绘制曲线中
        self.curve1.setData(self.data1)

#
# if __name__ == '__main__':
#     # app = QApplication(sys.argv)
#     # window = Ui_MainWindow()
#     # myWin = MyGraphWindow()
#     # myWin.show()
#     # sys.exit(app.exec_())
#     usb = USB()
#     usb.write(2.5)
#     usb.sample()

