#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from PyQt5 import QtCore
from .gui.ptree import Params
from .gui.wgiusas import WGiuSAS
from .model import GiSASModel


class Controller(QtCore.QObject):
    sendParameters = QtCore.pyqtSignal(dict, dict)
    calculateSignal = QtCore.pyqtSignal()
    emitDataSignal = QtCore.pyqtSignal()
    loadModelParametersSignal = QtCore.pyqtSignal(dict)

    def __init__(self, parent=None):
        super(Controller, self).__init__(parent)
        self.createModel()
        self.createWindows()
        self.connectSignals()
        self.loadSettings()
        self.connectParamsSignals()
        self.start()

    def createModel(self):
        self.gmodelThread = QtCore.QThread()
        self.gmodel = GiSASModel()
        self.gmodel.moveToThread(self.gmodelThread)

    def loadSettings(self):
        self.settings = QtCore.QSettings()
        self.loadModelParameters()
        self.wgiusas.loadSettings()
        self.wparams.loadSettings()
        self.workDir = self.settings.value('WGiuSAS/workDir', '')
        self.sendParameters.emit(self.wgiusas.tabs.imageParameters(), self.wgiusas.tabs.checkBoxesState())
        self.calculateSignal.emit()
        self.emitDataSignal.emit()

    def saveSettings(self):
        self.wgiusas.saveSettings()
        self.wparams.saveSettings()
        self.settings.setValue('WGiuSAS/workDir', self.workDir)

    def createWindows(self):
        self.wgiusas = WGiuSAS(controller=self)
        self.wparams = Params(controller=self)
        self.wparams.show()

    def connectSignals(self):
        self.sendParameters.connect(self.gmodel.setStartingParameters)
        self.calculateSignal.connect(self.gmodel.calculate)
        self.emitDataSignal.connect(self.gmodel.emitData)
        self.wgiusas.closeEventSignal.connect(self.closeAll)
        self.wgiusas.tabs.bkgOpenSignal.connect(self.setWorkDir)
        self.wgiusas.tabs.bkgOpenSignal.connect(self.gmodel.openBkg)
        self.wgiusas.tabs.bkgCheckBox.clicked.connect(self.gmodel.setBkgState)
        self.wgiusas.tabs.frameOpenSignal.connect(self.setWorkDir)
        self.wgiusas.tabs.frameOpenSignal.connect(self.gmodel.openFrame)
        self.wgiusas.tabs.floodOpenSignal.connect(self.setWorkDir)
        self.wgiusas.tabs.floodOpenSignal.connect(self.gmodel.openFlood)
        self.wgiusas.tabs.floodCheckBox.clicked.connect(self.gmodel.setFloodState)
        self.wgiusas.tabs.darkOpenSignal.connect(self.setWorkDir)
        self.wgiusas.tabs.darkOpenSignal.connect(self.gmodel.openDark)
        self.wgiusas.tabs.darkCheckBox.clicked.connect(self.gmodel.setDarkState)
        self.wgiusas.tabs.calibrationSignal.connect(self.gmodel.setParameters)
        self.wgiusas.actionRotateImage.triggered.connect(self.gmodel.rotateImage)
        self.wgiusas.actionFlipImageH.triggered.connect(self.gmodel.flipImageH)
        self.wgiusas.actionFlipImageV.triggered.connect(self.gmodel.flipImageV)
        self.wgiusas.actionLogarithmicScale.triggered[bool].connect(self.gmodel.switchLog)
        self.wgiusas.plot2DView.setBeamCenterSignal.connect(self.gmodel.setBeamCenter)
        self.wgiusas.plot2DView.setBeamCenterSignal.connect(self.wparams.setBeamCenter)
        self.gmodel.data2dSignal.connect(self.wgiusas.show2d)
        self.gmodel.errorSignal.connect(self.wgiusas.showError)
        self.wgiusas.plot2DView.setHROIDataSignal.connect(self.gmodel.calcHCut)
        self.wgiusas.plot2DView.setVROIDataSignal.connect(self.gmodel.calcVCut)
        self.gmodel.cutHValuesSignal.connect(self.wgiusas.plotHROIData)
        self.gmodel.cutVValuesSignal.connect(self.wgiusas.plotVROIData)
        self.gmodelThread.finished.connect(self.gmodel.saveSettings)
        self.gmodel.saveModelParametersSignal.connect(self.saveModelParameters)
        self.gmodel.changeCutUnitsSignal.connect(self.wgiusas.changeCutUnits)
        self.gmodel.changeCutUnitsSignal.connect(self.wgiusas.plot2DView.leftAxis.changeUnits)
        self.gmodel.changeCutUnitsSignal.connect(self.wgiusas.plot2DView.bottomAxis.changeUnits)
        self.gmodel.changeHCutSizeSignal.connect(self.wgiusas.plot2DView.changeHCutSize)
        self.gmodel.changeVCutSizeSignal.connect(self.wgiusas.plot2DView.changeVCutSize)
        self.loadModelParametersSignal.connect(self.gmodel.loadSettings)
        self.wgiusas.plot2DView.leftAxis.changeRangeSignal.connect(self.gmodel.calcVRange)
        self.wgiusas.plot2DView.bottomAxis.changeRangeSignal.connect(self.gmodel.calcHRange)
        self.gmodel.verticalRangeSignal.connect(self.wgiusas.plot2DView.leftAxis.setRealRange)
        self.gmodel.horizontalRangeSignal.connect(self.wgiusas.plot2DView.bottomAxis.setRealRange)

    def connectParamsSignals(self):
        for group in self.wparams.params.children():
            for child in group.children():
                child.sigValueChanging.connect(lambda p, v: self.gmodel.setParameters({p.name(): v}))
                child.sigValueChanged.connect(lambda p, v: self.gmodel.setParameters({p.name(): v}))
                child.sigValueChanged.emit(child, child.value())

    def start(self):
        self.gmodelThread.start()
        self.wgiusas.show()

    def setWorkDir(self, filepath):
        self.workDir = os.path.dirname(filepath)

    def closeAll(self):
        self.saveSettings()
        self.wparams.close()
        self.gmodelThread.quit()

    def saveModelParameters(self, params):
        for param in params:
            self.settings.setValue('Model/{}'.format(param), params[param])

    def loadModelParameters(self):
        self.loadModelParametersSignal.emit(
            {k.split('/')[-1]: self.settings.value(k) for k in self.settings.allKeys() if k.startswith('Model/')}
        )
