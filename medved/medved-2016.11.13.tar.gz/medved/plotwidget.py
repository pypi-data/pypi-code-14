#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtWidgets
import pyqtgraph as pg


class PlotWidget(pg.PlotWidget):
    exportSignal = QtCore.pyqtSignal(str)

    def __init__(self, parent=None, background='default', **kargs):
        super(PlotWidget, self).__init__(parent, background, **kargs)
        self.plotItem.vb.menu.addSeparator()
        self.exportAction = self.plotItem.vb.menu.addAction('Export data...')
        self.plotItem.vb.menu.addSeparator()
        self.exportAction.triggered.connect(self.exportData)

    def exportData(self):
        # noinspection PyCallByClass,PyTypeChecker,PyArgumentList
        filename = QtWidgets.QFileDialog.getSaveFileName(self, 'Save data into file')[0]
        if filename:
            self.exportSignal.emit(filename)
