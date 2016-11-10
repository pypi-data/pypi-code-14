#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
from PyQt5 import QtCore, QtWidgets
from .model import MedvedModel
from .wmedeval import QWMEDeval


class MedvedController(QtCore.QObject):
    def __init__(self):
        super(MedvedController, self).__init__()
        self.settings = QtCore.QSettings()
        self.createModel()
        self.createWindows()
        self.connectSignals()
        self.loadSettings()
        self.start()
        self.currentFourier = None
        self.currentData = None
        self.fourierPlot = None
        self.dataPlot = None
        self.wpogress = None

    def createModel(self):
        self.model = MedvedModel()

    def loadSettings(self):
        self.wmedved.loadSettings()
        self.wavelength = float(self.settings.value('WMedved/wavelength', '0.7'))
        self.wmedved.wlEdit.setText(str(self.wavelength))

    def saveSettings(self):
        self.wmedved.saveSettings()
        self.settings.setValue('WMedved/wavelength', self.wavelength)

    def createWindows(self):
        self.wmedved = QWMEDeval(self.settings, self)

    def connectSignals(self):
        self.wmedved.closeEventSignal.connect(self.closeAll)
        self.wmedved.chosenDirSignal.connect(self.setProgressWindow)
        self.wmedved.chosenDirSignal.connect(self.model.loadData)
        self.wmedved.dataPlot.exportSignal.connect(self.exportData)
        self.wmedved.fourierPlot.exportSignal.connect(self.exportFourier)
        self.model.loadErrorSignal.connect(self.removeProgressWindow)
        self.model.loadErrorSignal.connect(self.wmedved.showModelError)
        self.model.finishedLoadSignal.connect(self.wmedved.finishedLoad)
        self.model.finishedLoadSignal.connect(self.finishedLoad)
        self.wmedved.dataSliders.twothSlider.valueChanged.connect(self.showData2Th)
        self.wmedved.dataSliders.timeSlider.valueChanged.connect(self.showDataTime)
        self.wmedved.fourierSliders.twothSlider.valueChanged.connect(self.showFourier2Th)
        self.wmedved.fourierSliders.timeSlider.valueChanged.connect(self.showFourierTime)
        self.wmedved.updateFourierPlot.connect(self.redrawFourierPlot)
        self.wmedved.updateDataPlot.connect(self.redrawDataPlot)
        self.wmedved.wlEdit.textEdited.connect(self.changeWavelength)

    def setProgressWindow(self):
        self.wprogress = QtWidgets.QProgressDialog()
        self.wprogress.canceled.connect(self.model.cancelLoad)
        self.model.loadProgressSignal.connect(self.wprogress.setValue)
        self.model.setProgressMaximumSignal.connect(self.wprogress.setMaximum)
        self.model.setProgressLabelSignal.connect(self.wprogress.setLabelText)

    def removeProgressWindow(self):
        if self.wpogress:
            self.wprogress.canceled.disconnect(self.model.cancelLoad)
            self.model.loadProgressSignal.disconnect(self.wprogress.setValue)
            self.model.setProgressMaximumSignal.disconnect(self.wprogress.setMaximum)
            self.model.setProgressLabelSignal.disconnect(self.wprogress.setLabelText)
            self.wpogress = None

    def changeWavelength(self, wl):
        self.wavelength = float(wl)
        self.redrawFourierPlot()
        self.redrawDataPlot()

    def finishedLoad(self):
        self.removeProgressWindow()
        self.wmedved.dataSliders.imageView.setImage(self.model.data[:, 1, :])
        self.wmedved.dataSliders.timeSlider.valueChanged.emit(0)
        self.wmedved.fourierSliders.timeSlider.valueChanged.emit(0)
        self.redrawFourierPlot()

    def showData2Th(self, value):
        self.currentData = self.showData2Th, value
        if self.model.data is None:
            return
        x, y = self.model.datarange, self.model.data[value, 1, :]
        self.wmedved.dataSliders.plot.plot(x, y, pen='g', clear=True)
        self.wmedved.dataSliders.twothEdit.setText(str(self.model.data[value, 0, 0]))
        self.wmedved.dataSliders.imageView.drawArea(value, self.wmedved.dataSliders.twothSlider.orientation())
        self.dataPlot = x, y

    def showDataTime(self, value):
        self.wmedved.dataSliders.timeEdit.setText(str(value))
        self.currentData = self.showDataTime, value
        if self.model.data is None:
            return
        x, y = self.model.data[:, 0, value], self.model.data[:, 1, value]
        if self.wmedved.action2Theta.isChecked():
            pass
        elif self.wmedved.actionD.isChecked():
            x = self.wavelength / 2 / np.sin(np.radians(x) / 2)
        else:
            x = (self.wavelength / 2 / np.sin(np.radians(x) / 2)) ** 2
        self.wmedved.dataSliders.plot.plot(x, y, pen='g', clear=True)
        self.wmedved.dataSliders.imageView.drawArea(value, self.wmedved.dataSliders.timeSlider.orientation())
        self.dataPlot = x, y

    def showFourier2Th(self, value):
        self.wmedved.fourierSliders.twothEdit.setText(str(value))
        self.currentFourier = self.showFourier2Th, value
        params = {'pen': 'g', 'symbol': None}
        if self.model.fdata is None:
            return
        if self.wmedved.actionImaginary.isChecked():
            y = self.model.fdata[value, :].imag
        elif self.wmedved.actionAmplitude.isChecked():
            y = self.model.absolute[value, :]
        elif self.wmedved.actionPhase.isChecked():
            y = self.model.phase[value, :]
            params = {'pen': None, 'symbol': 'o'}
        else:
            y = self.model.fdata[value, :].real
        x = self.model.frange1
        self.wmedved.fourierSliders.plot.plot(x, y, clear=True, **params)
        self.drawPiPlot(params['symbol'])
        self.wmedved.fourierSliders.imageView.drawArea(value, self.wmedved.dataSliders.twothSlider.orientation())
        self.fourierPlot = x, y

    def showFourierTime(self, value):
        self.wmedved.fourierSliders.timeEdit.setText(str(value))
        self.currentFourier = self.showFourierTime, value
        if self.model.fdata is None:
            return
        params = {'pen': 'g', 'symbol': None}
        if self.wmedved.actionImaginary.isChecked():
            y = self.model.fdata[:, value].imag
        elif self.wmedved.actionAmplitude.isChecked():
            y = self.model.absolute[:, value]
        elif self.wmedved.actionPhase.isChecked():
            y = self.model.phase[:, value]
            params = {'pen': None, 'symbol': 'o'}
        else:
            y = self.model.fdata[:, value].real
        if self.wmedved.action2Theta.isChecked():
            x = self.model.data[:, 0, value]  # two theta
        elif self.wmedved.actionD.isChecked():
            x = self.wavelength / 2 / np.sin(np.radians(self.model.data[:, 0, value]) / 2)
        else:
            x = (self.wavelength / 2 / np.sin(np.radians(self.model.data[:, 0, value]) / 2)) ** 2
        self.drawPiPlot(params['symbol'])
        self.wmedved.fourierSliders.plot.plot(x, y, clear=True, **params)
        self.wmedved.fourierSliders.imageView.drawArea(value, self.wmedved.dataSliders.timeSlider.orientation())
        self.fourierPlot = x, y

    def drawPiPlot(self, symbol):
        if symbol:
            self.wmedved.fourierSliders.plot.plotItem.axes['left']['item'].setTicks(
                [[(-180, u'-π'), (-90, u'-π/2'), (0, u'0'), (90, u'π/2'), (180, u'π')]]
            )

    def start(self):
        self.wmedved.show()

    def closeAll(self):
        self.saveSettings()

    def redrawFourierPlot(self):
        if self.currentFourier:
            self.currentFourier[0](self.currentFourier[1])
        if self.model.fdata is None:
            return
        if self.wmedved.actionAmplitude.isChecked():
            fourier2d = self.model.absolute
        elif self.wmedved.actionPhase.isChecked():
            fourier2d = self.model.phase
        elif self.wmedved.actionImaginary.isChecked():
            fourier2d = self.model.fdata.imag
        else:
            fourier2d = self.model.fdata.real
        self.wmedved.fourierSliders.imageView.setImage(fourier2d)

    def redrawDataPlot(self):
        if self.currentData:
            self.currentData[0](self.currentData[1])

    def exportFourier(self, filename):
        if self.fourierPlot:
            np.savetxt(filename, np.array(self.fourierPlot).T)

    def exportData(self, filename):
        if self.dataPlot:
            np.savetxt(filename, np.array(self.dataPlot).T)
