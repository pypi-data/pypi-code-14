#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import numpy as np
from scipy import fftpack
from PyQt5 import QtCore
from . import filereader


class MedvedModel(QtCore.QObject):
    setProgressLabelSignal = QtCore.pyqtSignal(str)
    finishedLoadSignal = QtCore.pyqtSignal(int, int, int, int, str, list)
    loadErrorSignal = QtCore.pyqtSignal(str)
    loadProgressSignal = QtCore.pyqtSignal(int)
    setProgressMaximumSignal = QtCore.pyqtSignal(int)

    def __init__(self, parent=None):
        super(MedvedModel, self).__init__(parent)
        self.data = self.fdata = None
        self.canceled = True
        self.filereader = filereader.FileReader(self)

    def loadData(self, dire):
        self.canceled = False
        self.loadFiles(dire)

    def loadFiles(self, dire):
        self.setProgressLabelSignal.emit('Reading files...')
        try:
            self.filereader.read(dire)
        except filereader.FileReaderError as error:
            msg = str(error)
            if msg:
                self.loadErrorSignal.emit(msg)
            self.data = None
            self.files = []
        else:
            self.data = np.empty(self.filereader.dataFiles[0].shape + (len(self.filereader.dataFiles),))
            for i, d in enumerate(self.filereader.dataFiles):
                self.data[:, :, i] = d
            self.datarange = np.arange(self.data.shape[2])
            self.files = self.filereader.files
            self.calculateFourier()
            self.canceled = True
            if self.data is not None:
                self.finishedLoadSignal.emit(self.data.shape[2]-1, self.fdata.shape[1]-1,
                                             self.data.shape[0]-1, self.fdata.shape[0]-1,
                                             os.path.basename(dire), self.files)

    def calculateFourier(self):
        data = []
        self.setProgressLabelSignal.emit('Calculating Fourier...')
        self.setProgressMaximumSignal.emit(self.data[:, 1, :].shape[0])
        for i, line in enumerate(self.data[:, 1, :], 1):
            # noinspection PyArgumentList
            QtCore.QCoreApplication.processEvents()
            if self.canceled:
                return
            data.append(fftpack.fft(line))
            self.loadProgressSignal.emit(i)
        self.fdata = np.array(data)
        self.frange1 = np.arange(self.fdata.shape[1])
        self.absolute = np.absolute(self.fdata)
        self.phase = np.angle(self.fdata, deg=True)

    def cancelLoad(self):
        self.canceled = True
