# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/main_1.ui'
#
# Created: Mon Sep 26 23:25:57 2016
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
        MainWindow.resize(909, 356)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setContentsMargins(-1, -1, 116, -1)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.headband = QtGui.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.headband.setFont(font)
        self.headband.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.headband.setObjectName(_fromUtf8("headband"))
        self.verticalLayout.addWidget(self.headband)
        self.hs_0 = QtGui.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.hs_0.setFont(font)
        self.hs_0.setObjectName(_fromUtf8("hs_0"))
        self.verticalLayout.addWidget(self.hs_0)
        self.hs_1 = QtGui.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.hs_1.setFont(font)
        self.hs_1.setObjectName(_fromUtf8("hs_1"))
        self.verticalLayout.addWidget(self.hs_1)
        self.hs_2 = QtGui.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.hs_2.setFont(font)
        self.hs_2.setObjectName(_fromUtf8("hs_2"))
        self.verticalLayout.addWidget(self.hs_2)
        self.hs_3 = QtGui.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.hs_3.setFont(font)
        self.hs_3.setObjectName(_fromUtf8("hs_3"))
        self.verticalLayout.addWidget(self.hs_3)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.instance_list = QtGui.QListWidget(self.centralwidget)
        self.instance_list.setObjectName(_fromUtf8("instance_list"))
        self.horizontalLayout.addWidget(self.instance_list)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.btn_start = QtGui.QPushButton(self.centralwidget)
        self.btn_start.setObjectName(_fromUtf8("btn_start"))
        self.gridLayout.addWidget(self.btn_start, 1, 0, 1, 1)
        self.btn_load = QtGui.QPushButton(self.centralwidget)
        self.btn_load.setObjectName(_fromUtf8("btn_load"))
        self.gridLayout.addWidget(self.btn_load, 2, 0, 1, 1)
        self.btn_stop = QtGui.QPushButton(self.centralwidget)
        self.btn_stop.setObjectName(_fromUtf8("btn_stop"))
        self.gridLayout.addWidget(self.btn_stop, 1, 2, 1, 1)
        self.btn_pause = QtGui.QPushButton(self.centralwidget)
        self.btn_pause.setObjectName(_fromUtf8("btn_pause"))
        self.gridLayout.addWidget(self.btn_pause, 1, 1, 1, 1)
        self.clock = QtGui.QLCDNumber(self.centralwidget)
        self.clock.setObjectName(_fromUtf8("clock"))
        self.gridLayout.addWidget(self.clock, 0, 0, 1, 3)
        self.btn_settings = QtGui.QPushButton(self.centralwidget)
        self.btn_settings.setObjectName(_fromUtf8("btn_settings"))
        self.gridLayout.addWidget(self.btn_settings, 2, 1, 1, 1)
        self.horizontalLayout.addLayout(self.gridLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 909, 27))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtGui.QToolBar(MainWindow)
        self.toolBar.setObjectName(_fromUtf8("toolBar"))
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.toolBar_2 = QtGui.QToolBar(MainWindow)
        self.toolBar_2.setObjectName(_fromUtf8("toolBar_2"))
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar_2)
        self.tollBar_3 = QtGui.QToolBar(MainWindow)
        self.tollBar_3.setObjectName(_fromUtf8("tollBar_3"))
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.tollBar_3)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "IDC", None))
        self.headband.setText(_translate("MainWindow", "HeadBand  ", None))
        self.hs_0.setText(_translate("MainWindow", "HS_0  ", None))
        self.hs_1.setText(_translate("MainWindow", "HS_1  ", None))
        self.hs_2.setText(_translate("MainWindow", "HS_2  ", None))
        self.hs_3.setText(_translate("MainWindow", "HS_3  ", None))
        self.btn_start.setText(_translate("MainWindow", "Start", None))
        self.btn_load.setText(_translate("MainWindow", "Load", None))
        self.btn_stop.setText(_translate("MainWindow", "Stop", None))
        self.btn_pause.setText(_translate("MainWindow", "Pause", None))
        self.btn_settings.setText(_translate("MainWindow", "Settings", None))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar", None))
        self.toolBar_2.setWindowTitle(_translate("MainWindow", "toolBar_2", None))
        self.tollBar_3.setWindowTitle(_translate("MainWindow", "toolBar_3", None))

