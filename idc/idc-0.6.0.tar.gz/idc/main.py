# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/main.ui'
#
# Created: Sat Aug 27 12:57:17 2016
#      by: PyQt4 UI code generator 4.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(1128, 825)
        self.centralwidget = QtGui.QWidget(MainWindow)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.video_play = ControlVideoPlay(self.centralwidget)
        self.video_play.setObjectName(_fromUtf8("video_play"))



        self.gridLayout.addWidget(self.video_play, 0, 0, 1, 2, QtCore.Qt.AlignHCenter)
        self.video_cap = ControlWindow(self.centralwidget)
        self.video_cap.setObjectName(_fromUtf8("video_cap"))
        self.gridLayout.addWidget(self.video_cap, 1, 0, 1, 2)
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.btn_start = QtGui.QPushButton(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_start.sizePolicy().hasHeightForWidth())
        self.btn_start.setSizePolicy(sizePolicy)
        self.btn_start.setObjectName(_fromUtf8("btn_start"))
        self.gridLayout_2.addWidget(self.btn_start, 0, 3, 1, 1)
        self.btn_load = QtGui.QPushButton(self.centralwidget)
        self.btn_load.setObjectName(_fromUtf8("btn_load"))
        self.gridLayout_2.addWidget(self.btn_load, 2, 3, 1, 1)
        self.btn_stop = QtGui.QPushButton(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_stop.sizePolicy().hasHeightForWidth())
        self.btn_stop.setSizePolicy(sizePolicy)
        self.btn_stop.setObjectName(_fromUtf8("btn_stop"))
        self.gridLayout_2.addWidget(self.btn_stop, 1, 3, 1, 1)
        self.btn_conf = QtGui.QPushButton(self.centralwidget)
        self.btn_conf.setObjectName(_fromUtf8("btn_conf"))
        self.gridLayout_2.addWidget(self.btn_conf, 3, 3, 1, 1)
        self.clock = QtGui.QLCDNumber(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.clock.sizePolicy().hasHeightForWidth())
        self.clock.setSizePolicy(sizePolicy)
        self.clock.setObjectName(_fromUtf8("clock"))
        self.gridLayout_2.addWidget(self.clock, 0, 2, 1, 1)
        self.gridLayout.addLayout(self.gridLayout_2, 1, 2, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1128, 27))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtGui.QToolBar(MainWindow)
        self.toolBar.setObjectName(_fromUtf8("toolBar"))
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "IDC", None))
        self.btn_start.setText(_translate("MainWindow", "Start", None))
        self.btn_load.setText(_translate("MainWindow", "Load", None))
        self.btn_stop.setText(_translate("MainWindow", "Stop", None))
        self.btn_conf.setText(_translate("MainWindow", "Settings", None))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar", None))

from gui import ControlVideoPlay, ControlWindow
