#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtWidgets
from .ui.wtab import Ui_tabWidget
from . import pyqt2bool as _


class WTabs(QtWidgets.QTabWidget, Ui_tabWidget):
    frameOpenSignal = QtCore.pyqtSignal(str)
    darkOpenSignal = QtCore.pyqtSignal(str)
    floodOpenSignal = QtCore.pyqtSignal(str)
    bkgOpenSignal = QtCore.pyqtSignal(str)
    calibrationSignal = QtCore.pyqtSignal(dict)

    def __init__(self, controller, parent=None):
        super(WTabs, self).__init__(parent)
        self.controller = controller
        self.setupUi(self)

    def saveSettings(self):
        s = self.controller.settings
        s.setValue('WGiuSAS/frame', self.frameEdit.text())
        s.setValue('WGiuSAS/dark', self.darkEdit.text())
        s.setValue('WGiuSAS/darkCheck', self.darkCheckBox.isChecked())
        s.setValue('WGiuSAS/flood', self.floodEdit.text())
        s.setValue('WGiuSAS/floodCheck', self.floodCheckBox.isChecked())
        s.setValue('WGiuSAS/bkg', self.bkgEdit.text())
        s.setValue('WGiuSAS/bkgCheck', self.bkgCheckBox.isChecked())

    def loadSettings(self):
        s = self.controller.settings
        self.frameEdit.setText(s.value('WGiuSAS/frame', ''))
        self.darkEdit.setText(s.value('WGiuSAS/dark', ''))
        self.darkCheckBox.setChecked(_(s.value('WGiuSAS/darkCheck', False)))
        self.floodEdit.setText(s.value('WGiuSAS/flood', ''))
        self.floodCheckBox.setChecked(_(s.value('WGiuSAS/floodCheck', False)))
        self.bkgEdit.setText(s.value('WGiuSAS/bkg', ''))
        self.bkgCheckBox.setChecked(_(s.value('WGiuSAS/bkgCheck', False)))

    def _openFrame(self, signal, edit, frameType):
        # noinspection PyCallByClass,PyTypeChecker
        frame = QtWidgets.QFileDialog.getOpenFileName(self,
                                                  'Open a {}frame'.format(frameType),
                                                  self.controller.workDir,
                                                  '{}Frames (*.edf *.cbf)'.format(frameType))[0]
        if frame:
            signal.emit(frame)
            edit.setText(frame)

    @QtCore.pyqtSlot()
    def on_openFrameButton_clicked(self):
        self._openFrame(self.frameOpenSignal, self.frameEdit, '')

    @QtCore.pyqtSlot()
    def on_openDarkButton_clicked(self):
        self._openFrame(self.darkOpenSignal, self.darkEdit, 'Dark ')

    @QtCore.pyqtSlot()
    def on_openFloodButton_clicked(self):
        self._openFrame(self.floodOpenSignal, self.floodEdit, 'Flood ')

    @QtCore.pyqtSlot()
    def on_openBkgButton_clicked(self):
        self._openFrame(self.bkgOpenSignal, self.bkgEdit, 'Background ')

    def imageParameters(self):
        return {
            'frame': self.frameEdit.text(),
            'dark': self.darkEdit.text(),
            'flood': self.floodEdit.text(),
            'bkg': self.bkgEdit.text(),
        }

    def checkBoxesState(self):
        return {
            'applyBkg': self.bkgCheckBox.isChecked(),
            'applyFlood': self.floodCheckBox.isChecked(),
            'applyDark': self.darkCheckBox.isChecked(),
        }
