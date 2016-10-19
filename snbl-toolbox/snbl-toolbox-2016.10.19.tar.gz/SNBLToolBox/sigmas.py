#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import division
import os
import re
import math
from multiprocessing import Pool, cpu_count
from PyQt5 import QtCore, QtGui, QtWidgets
from cryio.cbfimage import CbfHeader
# noinspection PyUnresolvedReferences
from .ui import resources_rc
from .convert import FilesPage as _FilesPage, Page, ConvertPage


REGEXP1 = re.compile(r'(\d+)p?.chi$')
REGEXP2 = re.compile(r'(\d+)p_(\d+).chi$')


def convertChi(chi, i, norm, cut, dist, h, rcy, pixel, lineEnd, scale, ifrom=0, ito=0, monFolder=''):
    folder = os.path.join(os.path.dirname(chi), 'dat')
    if not os.path.exists(folder):
        os.mkdir(folder)

    chipath = os.path.basename(chi)
    name = REGEXP1.split(chipath)
    if len(name) == 3:
        basename, period = name[:2]
        cbfname = '%s%sp.cbf' % (basename, period)
    else:
        name = REGEXP2.split(chipath)
        basename, period, frame = name[:3]
        cbfname = '%s%sp_%s.cbf' % (basename, period, frame)
    newname = '%ss%d.dat' % (basename, i)
    newnamess = '%sss%d.dat' % (basename, i)
    news = open(os.path.join(folder, newname), 'w')
    newss = open(os.path.join(folder, newnamess), 'w')
    mon = 0
    if norm == 3:
        try:
            mon = CbfHeader(os.path.join(monFolder, cbfname))['Flux']
        except (KeyError, IOError):
            mon = 1

    iscale = 0
    iscalenum = 0
    th_ii = []

    for n, line in enumerate(open(chi, 'r')):
        if n < cut or line.startswith('#'):
            continue

        th, ii = line.split()
        th, ii = float(th), float(ii)
        if ii < 0:
            ii = 0
        if norm == 2 and ifrom <= th <= ito:
            iscale += ii
            iscalenum += 1
        th_ii.append((th, ii))

    for th, ii in th_ii:
        r = dist * math.tan(math.radians(th))

        if r < h:
            try:
                alpha = 2 * math.asin(r / h)
            except ValueError:
                return ()
            l = alpha * r

        elif r == h:
            l = math.pi * r

        else:
            try:
                beta = math.acos(rcy / r)
            except ValueError:
                return ()
            alpha = 2 * (math.pi - beta)
            l = alpha * r

        nn = l / pixel
        er = math.sqrt(ii) / math.sqrt(nn)
        news.write('%f %f %f%s' % (th, ii, er, lineEnd))
        if iscale and iscalenum:
            newss.write('%.10f %.10f %.10f%s' % (th, ii / iscale * iscalenum * scale,
                                                 er / iscale * iscalenum * scale, lineEnd))
        elif mon:
            newss.write('%.10f %.10f %.10f%s' % (th, ii / mon * scale, er / mon * scale, lineEnd))

    news.close()
    newss.close()
    return folder, newname, newnamess, iscale, iscalenum


class QChiConvert(QtCore.QObject):
    progressSignal = QtCore.pyqtSignal(tuple, int, int)
    errorSignal = QtCore.pyqtSignal()
    _checkOutputSignal = QtCore.pyqtSignal(tuple)

    def __init__(self, chis, args):
        QtCore.QObject.__init__(self)
        self.args = args
        self.chis = chis
        self._checkOutputSignal.connect(self.checkOutput)

    def terminateAll(self):
        self.pool.terminate()
        self.pool.join()

    def run(self):
        ncpu = cpu_count() + 1
        self.pool = Pool(ncpu if 2 <= ncpu <= 4 else 4)
        self.queueLength = len(self.chis)
        self.processed = 0
        for i, chi in enumerate(self.chis, 1):
            args = (chi, i) + self.args
            self.pool.apply_async(convertChi, args, callback=self._checkOutputSignal.emit)
        self.pool.close()

    def checkOutput(self, tpl):
        if tpl:
            self.processed += 1
            self.progressSignal.emit(tpl, self.processed, self.queueLength)
            if self.processed == self.queueLength:
                self.pool.join()
        else:
            self.errorSignal.emit()
            self.terminateAll()


class FilesPage(_FilesPage):
    @QtCore.pyqtSlot()
    def chooseFiles(self, what='*.chi *.xy'):
        _FilesPage.chooseFiles(self, what)

    @QtCore.pyqtSlot()
    def chooseFolder(self, what='.chi .xy'):
        _FilesPage.chooseFolder(self, what)


class OptionsPage(Page):
    def setupUi(self):
        self.distSpinBox = QtWidgets.QDoubleSpinBox()
        self.distSpinBox.setMaximum(10000)
        self.distSpinBox.setMinimum(0)
        self.distSpinBox.setDecimals(2)
        layout1 = QtWidgets.QHBoxLayout()
        layout1.addWidget(QtWidgets.QLabel('Detector - sample distance (mm)'))
        layout1.addWidget(self.distSpinBox)

        self.cutSpinBox = QtWidgets.QSpinBox()
        self.cutSpinBox.setMaximum(65535)
        self.cutSpinBox.setMinimum(0)
        layout2 = QtWidgets.QHBoxLayout()
        layout2.addWidget(QtWidgets.QLabel('Number of lines to cut'))
        layout2.addWidget(self.cutSpinBox)

        self.widthSpinBox = QtWidgets.QSpinBox()
        self.widthSpinBox.setMinimum(1)
        self.widthSpinBox.setMaximum(65535)
        layout3 = QtWidgets.QHBoxLayout()
        layout3.addWidget(QtWidgets.QLabel('Detector width (pixels)'))
        layout3.addWidget(self.widthSpinBox)

        self.pixelSpinBox = QtWidgets.QDoubleSpinBox()
        self.pixelSpinBox.setMinimum(0)
        self.pixelSpinBox.setMaximum(65536)
        self.pixelSpinBox.setDecimals(5)
        layout4 = QtWidgets.QHBoxLayout()
        layout4.addWidget(QtWidgets.QLabel('Pixel size (mm)'))
        layout4.addWidget(self.pixelSpinBox)

        self.beamxSpinBox = QtWidgets.QDoubleSpinBox()
        self.beamxSpinBox.setMinimum(0)
        self.beamxSpinBox.setMaximum(65536)
        self.beamxSpinBox.setDecimals(5)
        layout5 = QtWidgets.QHBoxLayout()
        layout5.addWidget(QtWidgets.QLabel('Beam center X'))
        layout5.addWidget(self.beamxSpinBox)

        self.beamySpinBox = QtWidgets.QDoubleSpinBox()
        self.beamySpinBox.setMinimum(-65536)
        self.beamySpinBox.setMaximum(65536)
        self.beamySpinBox.setDecimals(5)
        layout6 = QtWidgets.QHBoxLayout()
        layout6.addWidget(QtWidgets.QLabel('Beam center Y'))
        layout6.addWidget(self.beamySpinBox)

        self.noRadio = QtWidgets.QRadioButton('Nothing')
        self.noRadio.setChecked(True)

        self.bgRadio = QtWidgets.QRadioButton('Background')
        self.fromSpinBox = QtWidgets.QDoubleSpinBox()
        # noinspection PyUnresolvedReferences
        self.fromSpinBox.valueChanged[float].connect(lambda _: self.bgRadio.setChecked(True))
        self.toSpinBox = QtWidgets.QDoubleSpinBox()
        # noinspection PyUnresolvedReferences
        self.toSpinBox.valueChanged[float].connect(lambda _: self.bgRadio.setChecked(True))
        layout8 = QtWidgets.QHBoxLayout()
        layout8.addWidget(self.bgRadio)
        layout8.addWidget(QtWidgets.QLabel('from'))
        layout8.addWidget(self.fromSpinBox)
        layout8.addWidget(QtWidgets.QLabel('to'))
        layout8.addWidget(self.toSpinBox)

        self.monRadio = QtWidgets.QRadioButton('Monitor')
        self.monLineEdit = QtWidgets.QLineEdit()
        openButton = QtWidgets.QPushButton(QtGui.QIcon(':/open'), '')

        # noinspection PyUnresolvedReferences,PyUnusedLocal
        @openButton.clicked.connect
        @QtCore.pyqtSlot()
        def openDir():
            _dir = os.path.dirname(self.prevPage.fileList.item(0).text())
            # noinspection PyCallByClass,PyTypeChecker
            log = QtWidgets.QFileDialog.getExistingDirectory(self, 'Choose folder with cbf files', _dir)
            self.monLineEdit.setText(log)
            self.monRadio.setChecked(True)

        layout9 = QtWidgets.QHBoxLayout()
        layout9.addWidget(self.monRadio)
        layout9.addWidget(self.monLineEdit)
        layout9.addWidget(openButton)

        layout7 = QtWidgets.QVBoxLayout()
        layout7.addWidget(self.noRadio)
        layout7.addLayout(layout8)
        layout7.addLayout(layout9)

        self.scaleLineEdit = QtWidgets.QLineEdit()
        self.scaleLineEdit.setValidator(QtGui.QIntValidator())
        layout11 = QtWidgets.QHBoxLayout()
        layout11.addWidget(QtWidgets.QLabel('Scale all files by'))
        layout11.addWidget(self.scaleLineEdit)
        layout7.addLayout(layout11)
        gb = QtWidgets.QGroupBox('Normalize by')
        gb.setLayout(layout7)

        self.winRadio = QtWidgets.QRadioButton(r'Windows (\r\n)')
        self.linRadio = QtWidgets.QRadioButton(r'Unix (\n)')
        self.macRadio = QtWidgets.QRadioButton(r'Mac (\r)')
        layout10 = QtGui.QHBoxLayout()
        layout10.addWidget(self.winRadio)
        layout10.addWidget(self.linRadio)
        layout10.addWidget(self.macRadio)
        gb1 = QtWidgets.QGroupBox('End of line')
        gb1.setLayout(layout10)

        layoutn = QtWidgets.QVBoxLayout()
        layoutn.addLayout(layout1)
        layoutn.addLayout(layout2)
        layoutn.addLayout(layout3)
        layoutn.addLayout(layout4)
        layoutn.addLayout(layout5)
        layoutn.addLayout(layout6)
        layoutn.addWidget(gb)
        layoutn.addWidget(gb1)
        layoutn.addStretch()

        self.setLayout(layoutn)

    def initializePage(self):
        settings = QtCore.QSettings()
        self.distSpinBox.setValue(float(settings.value('SigmaS/dist', 100)))
        self.cutSpinBox.setValue(int(settings.value('SigmaS/cut', 4)))
        self.widthSpinBox.setValue(int(settings.value('SigmaS/width', 1475)))
        self.pixelSpinBox.setValue(float(settings.value('SigmaS/pixel', 0.172)))
        self.beamxSpinBox.setValue(float(settings.value('SigmaS/beamx', 0)))
        self.beamySpinBox.setValue(float(settings.value('SigmaS/beamy', 0)))
        self.fromSpinBox.setValue(float(settings.value('SigmaS/from', 10)))
        self.toSpinBox.setValue(float(settings.value('SigmaS/to', 20)))
        self.monLineEdit.setText(settings.value('SigmaS/mon', ''))
        self.scaleLineEdit.setText(settings.value('SigmaS/scale', '1'))
        norm = settings.value('SigmaS/norm', '')
        if not norm:
            self.noRadio.setChecked(True)
        elif norm == 'bkg':
            self.bgRadio.setChecked(True)
        elif norm == 'mon':
            self.monRadio.setChecked(True)

        lineEnd = settings.value('SigmaS/lineend', 'win')
        if lineEnd == 'mac':
            self.macRadio.setChecked(True)
        elif lineEnd == 'unx':
            self.linRadio.setChecked(True)
        else:
            self.winRadio.setChecked(True)

    def validatePage(self):
        settings = QtCore.QSettings()
        settings.setValue('SigmaS/dist', self.distSpinBox.value())
        settings.setValue('SigmaS/cut', self.cutSpinBox.value())
        settings.setValue('SigmaS/width', self.widthSpinBox.value())
        settings.setValue('SigmaS/pixel', self.pixelSpinBox.value())
        settings.setValue('SigmaS/beamx', self.beamxSpinBox.value())
        settings.setValue('SigmaS/beamy', self.beamySpinBox.value())
        settings.setValue('SigmaS/from', self.fromSpinBox.value())
        settings.setValue('SigmaS/to', self.toSpinBox.value())
        settings.setValue('SigmaS/mon', self.monLineEdit.text())
        settings.setValue('SigmaS/scale', self.scaleLineEdit.text())
        if self.macRadio.isChecked():
            lineEnd = 'mac'
        elif self.linRadio.isChecked():
            lineEnd = 'unx'
        else:
            lineEnd = 'win'
        settings.setValue('SigmaS/lineend', lineEnd)
        if self.bgRadio.isChecked():
            norm = 'bkg'
        elif self.monRadio.isChecked():
            norm = 'mon'
        else:
            norm = ''
        settings.setValue('SigmaS/norm', norm)
        return Page.validatePage(self)


class SigmaSWizard(QtWidgets.QWizard):
    terminateSignal = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        QtWidgets.QWizard.__init__(self, parent)
        filesPage = FilesPage()
        self.addPage(filesPage)
        self.addPage(OptionsPage(prevPage=filesPage))
        self.addPage(ConvertPage())
        self.setWindowTitle('Pylatus Sigma Scale')
        self.setOptions(QtWidgets.QWizard.NoBackButtonOnLastPage)
        self.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        matrix = QtGui.QTransform().rotate(-90)
        pixmap = QtGui.QPixmap(':/snbl').scaled(281, 151, QtCore.Qt.KeepAspectRatio,
                                                QtCore.Qt.SmoothTransformation).transformed(matrix)
        self.setPixmap(QtWidgets.QWizard.WatermarkPixmap, pixmap)
        self.loadSettings()
        self.setWindowIcon(QtGui.QIcon(':/scale'))
        self.stopped = False
        self.count = 1
        # noinspection PyUnresolvedReferences
        self.currentIdChanged[int].connect(self.checkPage)
        self.rejected.connect(self.terminate)
        self.workerThread = QtCore.QThread()
        self.errorShown = False

    def terminate(self):
        self.terminateSignal.emit()
        self.finish()

    def checkPage(self, page):
        if page == 2:
            self.convert()

    def convert(self):
        page1 = self.page(1)
        dist = page1.distSpinBox.value()
        cut = page1.cutSpinBox.value()
        pixel = page1.pixelSpinBox.value()
        beamy = page1.beamySpinBox.value()
        beamx = page1.beamxSpinBox.value()
        rcy = beamy * pixel
        h = beamx * pixel

        if page1.macRadio.isChecked():
            self.lineEnd = '\r'
        elif page1.linRadio.isChecked():
            self.lineEnd = '\n'
        else:
            self.lineEnd = '\r\n'

        norm = ifrom = ito = 1
        monFolder = ''
        if page1.bgRadio.isChecked():
            ifrom = page1.fromSpinBox.value()
            ito = page1.toSpinBox.value()
            norm = 2
        elif page1.monRadio.isChecked():
            norm = 3
            monFolder = page1.monLineEdit.text()

        scale = int(page1.scaleLineEdit.text() or 1)
        page0 = self.page(0)
        count = page0.fileList.count()
        self.scale, self.bufs, self.bufss = [], [], []
        chis = [page0.fileList.item(i).text() for i in range(count)]
        args = norm, cut, dist, h, rcy, pixel, self.lineEnd, scale, ifrom, ito, monFolder,
        self.worker = QChiConvert(chis, args)
        self.worker.moveToThread(self.workerThread)
        # noinspection PyUnresolvedReferences
        self.workerThread.started.connect(self.worker.run)
        self.terminateSignal.connect(self.worker.terminateAll)
        self.worker.progressSignal.connect(self.showProgress)
        self.worker.errorSignal.connect(self.showError)
        self.workerThread.start()

    def showProgress(self, results, processed, queueLength):
        folder, newname, newnamess, iscale, iscalenum = results
        self.bufs.append(newname)
        self.bufss.append(newnamess)
        self.scale.append((newnamess, iscale, iscalenum))
        page2 = self.page(2)
        page2.log.addItem('-> dat/%s' % newname)
        page2.log.scrollToBottom()
        page2.progress.setValue(100 * (processed + 1.) / queueLength)

        if processed == queueLength:
            exp = re.compile(r'(\d+).dat$')
            self.scale.sort(key=lambda k: int(exp.split(k[0])[1]))
            self.bufs.sort(key=lambda k: int(exp.split(k)[1]))
            self.bufss.sort(key=lambda k: int(exp.split(k)[1]))
            open(os.path.join(folder, 'scalers.dat'), 'w').write(self.lineEnd.join(
                ('%s %f %f' % s for s in self.scale)))
            open(os.path.join(folder, 'buffers.buf'), 'w').write(self.lineEnd.join(self.bufs))
            open(os.path.join(folder, 'bufferss.buf'), 'w').write(self.lineEnd.join(self.bufss))
            self.finish()

    def finish(self):
        self.stopped = True
        self.page(2).completeChanged.emit()
        self.workerThread.quit()
        self.workerThread.wait()

    def showError(self):
        if self.errorShown:
            return
        self.errorShown = True
        self.finish()
        # noinspection PyCallByClass,PyTypeChecker,PyArgumentList
        QtWidgets.QMessageBox.critical(self, 'Error in thread', 'It seems you have to swap beamX and beamY values')

    def closeEvent(self, event):
        self.saveSettings()
        event.accept()

    def loadSettings(self):
        settings = QtCore.QSettings()
        self.restoreGeometry(settings.value('SigmaS/Geometry', QtCore.QByteArray()))

    def saveSettings(self):
        settings = QtCore.QSettings()
        settings.setValue('SigmaS/Geometry', self.saveGeometry())
