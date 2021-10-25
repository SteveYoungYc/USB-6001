#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Py40 PyQt5 tutorial

This example shows a tooltip on
a window and a button.

author: Jan Bodnar
website: py40.com
last edited: January 2015
"""

import sys
from PyQt5.QtWidgets import (QWidget, QToolTip,
                             QPushButton, QApplication, QMainWindow)
from PyQt5.QtGui import QFont

from Communication import USB
from out import Ui_MainWindow


class FirstMainWin(QMainWindow):
    def __init__(self):  # self代表实例本身
        super(FirstMainWin, self).__init__()  # 调用父类初始化方法
        #设置主窗口的标题
        self.setWindowTitle("第一个窗口应用")
        #设置窗口的尺寸
        self.resize(400,300)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)

    usb = USB()
    usb.read()
    ui.changeNum(usb.dataStr)
    MainWindow.show()
    sys.exit(app.exec_())
