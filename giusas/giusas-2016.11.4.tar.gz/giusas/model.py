#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import math
import copy
import functools
import numpy as np
from PyQt5 import QtCore
import cryio


class GiSASModel(QtCore.QObject):
    T_ROT90, T_ROT180, T_ROT270, T_H_FLIP, T_V_FLIP = 1, 2, 3, 4, 5
    data2dSignal = QtCore.pyqtSignal(np.ndarray)
    errorSignal = QtCore.pyqtSignal(str)
    cutHValuesSignal = QtCore.pyqtSignal(np.ndarray, np.ndarray)
    cutVValuesSignal = QtCore.pyqtSignal(np.ndarray, np.ndarray)
    saveModelParametersSignal = QtCore.pyqtSignal(dict)
    changeCutUnitsSignal = QtCore.pyqtSignal(str, str)
    changeVCutSizeSignal = QtCore.pyqtSignal(int)
    changeHCutSizeSignal = QtCore.pyqtSignal(int)
    verticalRangeSignal = QtCore.pyqtSignal(float, float)
    horizontalRangeSignal = QtCore.pyqtSignal(float, float)

    def __init__(self, parent=None):
        super(GiSASModel, self).__init__(parent)
        self.setDefaultValues()
        self.dropImages()
        self.transformer = {
            self.T_ROT90: functools.partial(self.transformImages, functools.partial(np.rot90, k=self.T_ROT90)),
            self.T_ROT180: functools.partial(self.transformImages, functools.partial(np.rot90, k=self.T_ROT180)),
            self.T_ROT270: functools.partial(self.transformImages, functools.partial(np.rot90, k=self.T_ROT270)),
            self.T_H_FLIP: functools.partial(self.transformImages, np.flipud),
            self.T_V_FLIP: functools.partial(self.transformImages, np.fliplr),
        }

    def setDefaultValues(self):
        self.applyBkg = False
        self.applyDark = False
        self.applyFlood = False
        self.transmission = 1
        self.calibration = 1
        self.bkgCoef = 1
        self.thickness = 1
        self.concentration = 0
        self.lambda_ = 1
        self.dist = 100
        self.x0 = 100
        self.y0 = 100
        self.alphai = 1
        self.log = False
        self.pixel = 50
        self.vcutsize = 1
        self.hcutsize = 1
        self.cutunits = 'deg'
        self.framepath = ''
        self.framename = ''

    def switchLog(self, log):
        self.log = log
        self.emitData()

    def dropImages(self):
        self.frame = None
        self.dark = None
        self.bkg = None
        self.flood = None
        self.data = None
        self.transformations = []

    def openFrame(self, filepath, calculate=True):
        self.framepath = os.path.dirname(filepath)
        self.framename = os.path.basename(filepath)
        self.frame = self.openImage(filepath)
        if self.frame:
            self.frame.float()
            if calculate:
                self.calculate()
                self.emitData()

    def openBkg(self, filepath, calculate=True):
        self.bkg = self.openImage(filepath)
        if self.bkg:
            self.bkg.float()
            if calculate:
                self.calculate()
                self.emitData()

    def openFlood(self, filepath, calculate=True):
        self.flood = self.openImage(filepath)
        if self.flood:
            self.flood.float()
            if calculate:
                self.calculate()
                self.emitData()

    def openDark(self, filepath, calculate=True):
        self.dark = self.openImage(filepath)
        if self.dark:
            self.dark.float()
            if calculate:
                self.calculate()
                self.emitData()

    def calculate(self):
        self.transmission = 0
        frame = copy.deepcopy(self.frame)
        bkg = copy.deepcopy(self.bkg)
        flood = copy.deepcopy(self.flood)
        dark = copy.deepcopy(self.dark)
        frame, bkg, flood, dark = self.applyTransformations((frame, bkg, flood, dark))

        if dark and self.applyDark:
            if bkg:
                bkg.array -= dark.array
                # bkg.normalize()
            if frame:
                frame.array -= dark.array
                # frame.normalize()

        if frame:
            if bkg and self.applyBkg:
                if frame.transmission and bkg.transmission:
                    frame.array = (self.calibration * (frame.array - self.bkgCoef * bkg.array * frame.transmission * (
                        1 - self.concentration) / bkg.transmission) / frame.transmission / self.thickness)
                    self.transmission = frame.transmission / bkg.transmission
                else:
                    frame.array = self.calibration * (frame.array - self.bkgCoef * bkg.array)
            else:
                frame.array *= self.calibration
        self.data = frame

    def emitData(self):
        if self.data:
            data = self.data.array[:]
            if self.log:
                if self.applyDark or self.applyBkg or self.applyFlood:
                    data[data <= 0] = data.min() * 1e-10
                data = np.log(self.data.array)
            self.data2dSignal.emit(data)

    def setBkgState(self, state, calculate=True):
        self.applyBkg = state
        if calculate:
            self.calculate()
            self.emitData()

    def setDarkState(self, state, calculate=True):
        self.applyDark = state
        if calculate:
            self.calculate()
            self.emitData()

    def setFloodState(self, state, calculate=True):
        self.applyFlood = state
        if calculate:
            self.calculate()
            self.emitData()

    def openImage(self, filepath):
        if not filepath:
            return None
        try:
            frame = cryio.openImage(filepath)
        except (cryio.ImageError, IOError, OSError) as err:
            self.errorSignal.emit(err.strerror)
            return None
        else:
            return frame

    def setParameters(self, params, calculate=True):
        for param in params:
            if param in self.__dict__:
                getattr(self, 'set{}'.format(param.title()))(params[param])
        if calculate:
            self.calculate()
            self.emitData()

    def setCalibration(self, value):
        self.calibration = value

    def setCutunits(self, value):
        self.cutunits = value
        if 'pixels' in value:
            self.changeCutUnitsSignal.emit('pixel_x', 'pixel_y')
        elif value == 'q':
            self.changeCutUnitsSignal.emit('q_y', 'q_z')
        elif value == 'deg':
            self.changeCutUnitsSignal.emit('theta_f', 'alpha_f')

    def setHcutsize(self, value):
        self.hcutsize = int(value)
        self.changeHCutSizeSignal.emit(self.hcutsize)

    def setVcutsize(self, value):
        self.vcutsize = int(value)
        self.changeVCutSizeSignal.emit(self.vcutsize)

    def setThickness(self, value):
        if -1e-5 <= value <= 1e-5:
            self.errorSignal.emit('Sample thickness is to small!')
        else:
            self.thickness = value

    def setBkgcoef(self, value):
        self.bkgCoef = value

    def setConcentration(self, value):
        self.concentration = value

    def setLambda_(self, value):
        self.lambda_ = value
        self.calcConsts()

    def setDist(self, value):
        self.dist = value
        self.calcConsts()

    def setX0(self, value):
        self.x0 = value

    def setY0(self, value):
        self.y0 = value

    def setAlphai(self, value):
        self.alphai = math.radians(value)

    def setPixel(self, value):
        self.pixel = value
        self.calcConsts()

    def setStartingParameters(self, pimage=None, pchecks=None):
        if pimage:
            for key in pimage:
                getattr(self, 'open{}'.format(key.title()))(pimage[key], calculate=False)
        if pchecks:
            for key in pchecks:
                setattr(self, key, pchecks[key])

    def rotateImage(self):
        if self.transformations and self.transformations[-1] - 3 <= 0:
            self.transformations[-1] += 1
            if self.transformations[-1] >= 4:
                self.transformations.pop()
        else:
            self.transformations.append(self.T_ROT90)
        self.calculate()
        self.emitData()

    def flipImageH(self):
        # if it is the same transformation, as it was the last one, we just cancel the last one
        if self.transformations and self.transformations[-1] == self.T_H_FLIP:
            self.transformations.pop()
        else:
            self.transformations.append(self.T_H_FLIP)
        self.calculate()
        self.emitData()

    def flipImageV(self):
        # if it is the same transformation, as it was the last one, we just cancel the last one
        if self.transformations and self.transformations[-1] == self.T_V_FLIP:
            self.transformations.pop()
        else:
            self.transformations.append(self.T_V_FLIP)
        self.calculate()
        self.emitData()

    def applyTransformations(self, images):
        for t in self.transformations:
            images = self.transformer[t](images)
        return images

    def transformImages(self, transformation, images):
        _images = []
        for image in images:
            if image:
                image.array = transformation(image.array)
            _images.append(image)
        return _images

    def setBeamCenter(self, x, y):
        self.setX0(x)
        self.setY0(y)

    def calcHCut(self, data, coords, save=False, center=None):
        if data is None:
            return
        while data.ndim > 1:
            data = data.mean(axis=1)
        while coords.ndim > 2:
            coords = coords[:, :, 0]
        hcd = coords - coords[:, 0, np.newaxis]
        x = np.sqrt((hcd ** 2).sum(axis=0)) + coords[0][0]
        x = self.calcHCutValues(x)
        self.cutHValuesSignal.emit(x, data)
        self.saveCut(save, x, data, center, 'h')

    def calcHCutValues(self, x):
        if self.cutunits == 'calibrated pixels':
            x = x - self.x0
        elif self.cutunits == 'deg':
            x = np.degrees(self.thetaf(x))
        elif self.cutunits == 'q':
            x = self.qy(x)
        return x

    def thetaf(self, x):
        return np.arctan((x - self.x0) * self.pixdist)

    def qy(self, x):
        return self.qconst * np.sin(self.thetaf(x))

    def calcVCut(self, data, coords, save=False, center=None):
        if data is None:
            return
        while data.ndim > 1:
            data = data.mean(axis=0)
        while coords.ndim > 2:
            coords = coords[:, 0, :]
        hcd = coords - coords[:, 0, np.newaxis]
        y = np.sqrt((hcd ** 2).sum(axis=0)) + coords[1][0]
        y = self.calcVCutValues(y)
        self.cutVValuesSignal.emit(y, data)
        self.saveCut(save, y, data, center, 'v')

    def calcVCutValues(self, y):
        if self.cutunits == 'calibrated pixels':
            y = y - self.y0
        elif self.cutunits == 'deg':
            # noinspection PyTypeChecker
            y = np.degrees(self.alphaf(y))
        elif self.cutunits == 'q':
            y = self.qz(y)
        return y

    def alphaf(self, y):
        return np.arctan((y - self.y0) * self.pixdist) - self.alphai

    def qz(self, y):
        # noinspection PyTypeChecker
        return self.qconst * (math.sin(self.alphai) + np.sin(self.alphaf(y)))

    def calcConsts(self):
        self.qconst = 2 * math.pi / self.lambda_ * 10
        self.pixdist = self.pixel / self.dist

    def saveSettings(self):
        self.saveModelParametersSignal.emit({'transformations': ' '.join(str(i) for i in self.transformations)})

    def loadSettings(self, params):
        if 'transformations' in params:
            self.transformations = [int(t) for t in params['transformations'].split()]

    def saveCut(self, save, x, y, center, name):
        if not save or not self.framepath:
            return
        x0, y0 = center
        x0 = self.calcHCutValues(x0)
        y0 = self.calcVCutValues(y0)
        d = os.path.join(self.framepath, 'giusas_cuts')
        if not os.path.exists(d):
            os.mkdir(d)
        if self.cutunits == 'q':
            ux, uy = 'qy', 'qz'
        elif self.cutunits == 'deg':
            ux, uy = 'alpha_f', 'theta_f'
        else:
            ux, uy = 'pixel_x', 'pixel_y'
        fn = os.path.join(d, '{}_{}_{}_{:.3f}_{}_{:.3f}.dat'.format(self.framename, name, ux, x0, uy, y0))
        np.savetxt(fn, np.array((x, y)).T, header='{} I'.format(self.cutunits.replace(' ', '_')))

    def calcVRange(self, ymin, ymax):
        self.verticalRangeSignal.emit(self.calcVCutValues(ymin), self.calcVCutValues(ymax))

    def calcHRange(self, xmin, xmax):
        self.horizontalRangeSignal.emit(self.calcHCutValues(xmin), self.calcHCutValues(xmax))
