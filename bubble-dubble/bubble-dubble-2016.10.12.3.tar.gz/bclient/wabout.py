#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from bubble.bclient.ui.ui_wabout import Ui_WBubbleAbout
from bubble.bcommon.default import get_hg_hash


class WAboutBubble(QtWidgets.QDialog, Ui_WBubbleAbout):
    def __init__(self, parent=None):
        # noinspection PyArgumentList
        QtWidgets.QDialog.__init__(self, parent)
        self._parent = parent
        self.setupUi(self)
        lt = self.aboutLabel.text()
        lt = lt.replace('@', get_hg_hash())
        self.aboutLabel.setText(lt)
        self.setWindowIcon(QtGui.QIcon(':/swiss'))
        # noinspection PyCallByClass,PyTypeChecker
        QtCore.QTimer.singleShot(0.1, lambda: self.resize(0, 0))

    @QtCore.pyqtSlot()
    def on_closeButton_clicked(self):
        self.close()

    @QtCore.pyqtSlot()
    def on_aboutQtButton_clicked(self):
        # noinspection PyCallByClass,PyTypeChecker,PyArgumentList
        QtWidgets.QMessageBox.aboutQt(self)
