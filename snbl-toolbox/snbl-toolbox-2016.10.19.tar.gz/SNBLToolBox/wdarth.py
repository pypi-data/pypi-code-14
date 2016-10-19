#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import glob
from PyQt5 import QtCore, QtGui, QtWidgets
from cryio import ccp4image, parparser, cbfimage
from .ui.ui_wdarth import Ui_WDarth
from . import pyqt2bool


class WorkerSignals(QtCore.QObject):
    errorSignal = QtCore.pyqtSignal(str)
    progressSignal = QtCore.pyqtSignal(int)
    stopSignal = QtCore.pyqtSignal()
    finishedSignal = QtCore.pyqtSignal(object)


class Worker(QtCore.QRunnable):
    def __init__(self, params):
        QtCore.QRunnable.__init__(self)
        self.stop = False
        folder = params.pop('folder')
        self.folder = folder[:-1] if folder[-1] == '/' or folder[-1] == '\\' else folder
        self.params = params
        self.signals = WorkerSignals()
        self.signals.stopSignal.connect(self.stopIt)

    def stopIt(self):
        self.stop = True

    def parfile(self):
        self.par = parparser.ParParser(self.params['par'])

    def makemap(self):
        self.par.x = self.params['x']
        self.par.y = self.params['y']
        self.par.z = self.params['z']
        self.par.dQ = self.params['dQ']
        self.par.lorentz = self.params['lorentz']
        ccp4 = ccp4image.CCP4Image(self.par)
        for i, cbf in enumerate(self.cbflist, 1):
            if self.stop:
                break
            hdr = cbfimage.CbfHeader(cbf)
            ccp4.cbf2ccp4(hdr)
            self.signals.progressSignal.emit(i)
        if not self.stop:
            ccp4.save_map(self.mapname)
        self.signals.progressSignal.emit(len(self.cbflist))

    def run(self):
        self.basename = os.path.basename(self.folder)
        self.mapname = os.path.join(self.folder, '{}.ccp4'.format(self.basename))
        self.cbflist = glob.glob(os.path.join(self.folder, '*.cbf'))
        self.cbflist.sort()
        self.parfile()
        self.makemap()
        self.stopIt()
        self.signals.finishedSignal.emit(self)


class WorkerPool(QtCore.QObject):
    progressSignal = QtCore.pyqtSignal(int)
    finishedSignal = QtCore.pyqtSignal(list)

    def __init__(self, parent=None):
        QtCore.QObject.__init__(self, parent)
        # noinspection PyArgumentList
        self.pool = QtCore.QThreadPool.globalInstance()
        self.workers, self.errors = [], []

    def run(self, params):
        folder = params['folder']
        self.files = self.done = 0
        self.workers, self.errors = [], []
        for dirpath, dirnames, filenames in os.walk(folder):
            pars = glob.glob(os.path.join(dirpath, '*_cracker.par'))
            if not pars:
                continue
            p = params.copy()
            p['par'] = pars[0]
            p['folder'] = dirpath
            self.files += len(filenames)
            worker = Worker(p.copy())
            worker.signals.errorSignal.connect(self.workerError)
            worker.signals.progressSignal.connect(self.workerProgress)
            worker.signals.finishedSignal.connect(self.workerFinished)
            self.workers.append(worker)
        self.progressSignal.emit(0)
        for worker in self.workers:
            self.pool.start(worker)

    def stopIt(self):
        for worker in self.workers:
            worker.signals.stopSignal.emit()

    def workerProgress(self, i):
        self.done += i
        done = 100.0 * self.done / self.files
        self.progressSignal.emit(done)

    def workerError(self, folder):
        self.errors.append(folder)

    def workerFinished(self, worker):
        self.workers.remove(worker)
        if not self.workers:
            self.progressSignal.emit(100)
            self.finishedSignal.emit(self.errors)


class WDarth(QtWidgets.QDialog, Ui_WDarth):
    stopWorkerSignal = QtCore.pyqtSignal()
    runWorkerSignal = QtCore.pyqtSignal(dict)

    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self._parent = parent
        self.setupUi(self)
        intValidator = QtGui.QIntValidator()
        intValidator.setBottom(1)
        floatValidator = QtGui.QDoubleValidator()
        floatValidator.setBottom(1e-3)
        self.xLineEdit.setValidator(intValidator)
        self.yLineEdit.setValidator(intValidator)
        self.zLineEdit.setValidator(intValidator)
        self.dQLineEdit.setValidator(floatValidator)
        self.loadSettings()
        self.stopButton.setVisible(False)
        self.workerThread = QtCore.QThread()
        self.pool = WorkerPool()
        self.pool.moveToThread(self.workerThread)
        self.pool.progressSignal.connect(self.showProgress)
        self.pool.finishedSignal.connect(self.workerFinished)
        self.stopWorkerSignal.connect(self.pool.stopIt)
        self.runWorkerSignal.connect(self.pool.run)

    def showEvent(self, event):
        self.workerThread.start()

    def showError(self, errors):
        # noinspection PyCallByClass,PyArgumentList,PyTypeChecker
        QtWidgets.QMessageBox.critical(self,
                                       'Darth Vader error',
                                       'Datasets in folders\n{}\nare corrupted: it seems you have aborted the '
                                       'experiments because the headers are empty.\n It cannot be '
                                       'processed.'.format('\n'.join(errors)))

    def showProgress(self, value):
        self.runProgressBar.setFormat('{0}: %p%'.format('Reading files'))
        self.runProgressBar.setValue(value)

    def closeEvent(self, event):
        self.saveSettings()
        self.hide()
        self.stopWorkerSignal.emit()
        self.workerThread.quit()

    def saveSettings(self):
        settings = QtCore.QSettings()
        settings.setValue('WDarth/Geometry', self.saveGeometry())
        settings.setValue('WDarth/lastFolder', self.lastFolder)
        settings.setValue('WDarth/folder', self.folderLineEdit.text())
        settings.setValue('WDarth/x', self.xLineEdit.text())
        settings.setValue('WDarth/y', self.yLineEdit.text())
        settings.setValue('WDarth/z', self.zLineEdit.text())
        settings.setValue('WDarth/dQ', self.dQLineEdit.text())
        settings.setValue('WDarth/lorentz', self.lorentzCheckBox.isChecked())

    def loadSettings(self):
        settings = QtCore.QSettings()
        self.restoreGeometry(settings.value('WDarth/Geometry', QtCore.QByteArray()))
        self.lastFolder = settings.value('WDarth/lastFolder', u'')
        self.folderLineEdit.setText(settings.value('WDarth/folder', u''))
        self.xLineEdit.setText(settings.value('WDarth/x', '256'))
        self.yLineEdit.setText(settings.value('WDarth/y', '256'))
        self.zLineEdit.setText(settings.value('WDarth/z', '256'))
        self.dQLineEdit.setText(settings.value('WDarth/dQ', '0.6'))
        self.lorentzCheckBox.setChecked(pyqt2bool(settings.value('WDarth/lorentz', False)))

    @QtCore.pyqtSlot()
    def on_runButton_clicked(self):
        folder = self.folderLineEdit.text()
        if not folder or not os.path.exists(folder):
            return
        self.runButton.setVisible(False)
        self.stopButton.setVisible(True)
        params = {
            'folder': folder,
            'x': int(self.xLineEdit.text()),
            'y': int(self.yLineEdit.text()),
            'z': int(self.zLineEdit.text()),
            'dQ': float(self.dQLineEdit.text()),
            'lorentz': int(self.lorentzCheckBox.isChecked()),
        }
        self.runWorkerSignal.emit(params)

    def workerFinished(self, errors):
        self.runButton.setVisible(True)
        self.stopButton.setVisible(False)
        if errors:
            self.showError(errors)

    @QtCore.pyqtSlot()
    def on_stopButton_clicked(self):
        self.stopWorkerSignal.emit()

    @QtCore.pyqtSlot()
    def on_folderButton_clicked(self):
        # noinspection PyCallByClass,PyTypeChecker
        folder = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select directory', self.lastFolder)
        if not folder:
            return
        self.folderLineEdit.setText(folder)
        self.lastFolder = folder
