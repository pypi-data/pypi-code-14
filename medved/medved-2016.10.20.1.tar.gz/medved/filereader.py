#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from PyQt5 import QtCore
import numpy as np
import fortranformat as ff


class FileReaderError(Exception):
    pass


class FileReader(QtCore.QObject):
    def __init__(self, parent):
        super(FileReader, self).__init__(parent)
        self._parent = parent
        self.readable = False

    def read(self, folder):
        files = sorted(os.listdir(folder))
        self._parent.setProgressMaximumSignal.emit(len(files))
        self.files, self.dataFiles = [], []
        for i, f in enumerate(files):
            # noinspection PyArgumentList
            QtCore.QCoreApplication.processEvents()
            if self._parent.canceled:
                raise FileReaderError
            datafile = os.path.join(folder, f)
            if not os.path.isfile(datafile):
                continue
            if f.endswith('.hkl'):
                data = self.readhkl(datafile)
            else:
                try:
                    data = np.loadtxt(datafile)
                except ValueError as err:
                    print('Value error:', err)
                    continue
            self.dataFiles.append(data)
            self.files.append(f)
            self._parent.loadProgressSignal.emit(i)
        if not self.dataFiles:
            raise FileReaderError('There were no acceptable files')

    def readhkl(self, datafile):
        # noinspection PyUnresolvedReferences
        header = ff.FortranRecordReader('3I4,2F8.2')
        lst = []
        for line in open(datafile):
            try:
                line = header.read(line)
            except ValueError:
                break
            else:
                if None not in line:
                    lst.append(line)
        array = np.array(lst)
        array = array[np.lexsort((array[:, 2], array[:, 1], array[:, 0]))]  # sorting by l k h
        b = np.empty_like(array)
        it = np.nditer(array, flags=['multi_index'])
        hkl = np.array([0., 0., 0., 0., 0.])
        j, k = 0, 1
        first = True
        while not it.finished:
            index = it.multi_index[1]
            hkl[index] = it[0]
            if index == 4:
                if first:
                    first = False
                    _hkl = hkl.copy()
                elif np.array_equal(hkl[:3], _hkl[:3]):
                    k += 1
                    _hkl[3:] += hkl[3:]
                else:
                    _hkl[3:] /= k
                    b[j, :] = _hkl
                    _hkl = hkl.copy()
                    k = 1
                    j += 1
            it.iternext()
        array = np.c_[np.arange(j), b[:j, 3:], b[:j, :3]]
        return array
