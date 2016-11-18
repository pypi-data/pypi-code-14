#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import re
import copy
import sip
import multiprocessing as mp
import six
from PyQt5 import QtCore, QtGui, QtWidgets
import cryio
from cryio.cbfimage import CbfImage
from . import pyqt2bool
# noinspection PyUnresolvedReferences
from .ui import resources_rc


NEGATIVE_THRESHOLD = -3


def convertCbf(opts):
    folder = os.path.join(os.path.dirname(opts['images'][0]), opts['format'])
    angleInc = 0
    if six.PY3:
        try:
            os.mkdir(folder)
        except FileExistsError:
            pass
    else:
        try:
            os.mkdir(folder)
        except OSError:
            pass
    img = cryio.openImage(opts['images'][0])
    if isinstance(img, CbfImage):
        angleInc = img.header_dict['Angle_increment']
    for image in opts['images'][1:]:
        img += cryio.openImage(image)
    if opts['negative'] > NEGATIVE_THRESHOLD:
        img.array[img.array < 0] = opts['negative']
    if isinstance(img, CbfImage) and 'changeAngleIncrement' in opts and not opts['changeAngleIncrement']:
        img.header_dict['Angle_increment'] = angleInc
    if 'Pixel_size' in img.header:
        img.header['pixel_size'] = img.header['Pixel_size'][0]
    opts.update(img.header)
    newImg = os.path.join(folder, opts['name'])
    img.save(newImg, opts['format'], **opts)
    return '-> %s/%s' % (opts['format'], opts['name'])


class QCbfConvert(QtCore.QObject):
    progressSignal = QtCore.pyqtSignal(str, int, int)
    poolSignal = QtCore.pyqtSignal(str)

    def __init__(self, opts):
        QtCore.QObject.__init__(self)
        self.opts = opts
        self.poolSignal.connect(self.showProgress)

    def terminateAll(self):
        self.pool.terminate()
        self.pool.join()

    def simpleConversion(self):
        for cbf in self.opts['images']:
            name = '%s.%s' % (os.path.basename(cbf)[:-4], self.opts['format'])
            nargs = copy.deepcopy(self.opts)
            nargs.update({'images': (cbf,), 'name': name})
            yield nargs

    def makeChunk(self, i, images):
        args = copy.deepcopy(self.opts)
        name = '%s_%05d.%s' % ('_'.join(os.path.basename(images[0])[:-4].split('_')[:-1]), i, self.opts['format'])
        args.update({'images': images, 'name': name})
        return args

    def binFrames(self):
        i, images = 0, []
        for j, cbf in enumerate(self.opts['images']):
            images.append(cbf)
            if len(images) == self.opts['bintype']:
                i += 1
                chunk = self.makeChunk(i, images)
                yield chunk
                images = []
        converted = i * self.opts['bintype']
        if converted < len(self.opts['images']):
            i += 1
            yield self.makeChunk(i, self.opts['images'][converted:])

    def binPeriods(self):
        pattern = re.compile(r'.+_(\d+)p_(\d+)\.cbf$')
        self.opts['changeAngleIncrement'] = False

        def keyfunc(cbf):
            period, frame = map(int, pattern.split(cbf)[1:3])
            if not keyfunc.i:
                keyfunc.i = period
            if period > self.opts['bintype']:
                self.opts['bintype'] = period
            return frame
        keyfunc.i = 0

        try:
            self.opts['images'].sort(key=keyfunc)
        except KeyError:
            pass
        if keyfunc.i != 1:
            self.opts['bintype'] -= keyfunc.i - 1
        return self.binFrames()

    def convert(self):
        ncpu = mp.cpu_count()
        self.pool = mp.Pool(ncpu + 1 if 1 <= ncpu <= 5 else 5)
        if self.opts['binning']:
            if self.opts['bintype']:
                images = self.binFrames()
            else:
                images = self.binPeriods()
        else:
            images = self.simpleConversion()

        images = list(images)
        self.queueLength, self.converted = len(images), 0
        for chunk in images:
            if six.PY3:
                self.pool.apply_async(convertCbf, (chunk,), callback=self.poolSignal.emit,
                                      error_callback=self.showError)
            else:
                self.pool.apply_async(convertCbf, (chunk,), callback=self.poolSignal.emit)
            # self.poolSignal.emit(convertCbf(chunk))
        self.pool.close()

    def showError(self, err):
        print(err)

    def showProgress(self, fname):
        self.converted += 1
        self.progressSignal.emit(fname, self.converted, self.queueLength)
        if self.converted == self.queueLength:
            self.pool.join()


class Page(QtWidgets.QWizardPage):
    def __init__(self, parent=None, prevPage=None):
        QtWidgets.QWizardPage.__init__(self, parent)
        self.prevPage = prevPage
        self.setupUi()

    def setupUi(self):
        pass


class FilesPage(Page):
    # noinspection PyUnresolvedReferences
    def setupUi(self):
        folderButton = QtGui.QPushButton('Choose folder...')
        folderButton.clicked.connect(self.chooseFolder)

        filesButton = QtGui.QPushButton('Choose files...')
        filesButton.clicked.connect(self.chooseFiles)

        label = QtGui.QLabel('or')

        hlayout = QtGui.QHBoxLayout()
        hlayout.addWidget(folderButton)
        hlayout.addWidget(label)
        hlayout.addWidget(filesButton)
        hlayout.addStretch()

        self.fileList = QtGui.QListWidget()
        self.fileList.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)

        delButton = QtGui.QPushButton('Delete items')
        delButton.clicked.connect(self.delItems)

        clearButton = QtGui.QPushButton('Clear')
        clearButton.clicked.connect(self.clearItems)

        self.label = QtGui.QLabel('Selected files: 0')

        hlayout1 = QtGui.QHBoxLayout()
        hlayout1.addWidget(self.label)
        hlayout1.addStretch()
        hlayout1.addWidget(delButton)
        hlayout1.addWidget(clearButton)

        vlayout = QtGui.QVBoxLayout()
        vlayout.addLayout(hlayout)
        vlayout.addWidget(self.fileList)
        vlayout.addLayout(hlayout1)
        self.setLayout(vlayout)

    def initializePage(self):
        settings = QtCore.QSettings()
        self.lastFolder = settings.value('Convert/lastFolder', '')

    @QtCore.pyqtSlot()
    def chooseFolder(self, what='.cbf .edf'):
        # noinspection PyCallByClass,PyTypeChecker,PyArgumentList
        d = QtWidgets.QFileDialog.getExistingDirectory(self, 'Choose the folder with %s files' % what, self.lastFolder)
        if d:
            files = []
            for dirpath, dirnames, filenames in os.walk(d):
                for ext in what.split(' '):
                    files += [os.path.join(dirpath, f) for f in filenames if f.endswith(ext)]
                    # noinspection PyArgumentList
                    QtCore.QCoreApplication.processEvents()
            self.openFiles(files)

    @QtCore.pyqtSlot()
    def chooseFiles(self, what='*.cbf *.edf'):
        # noinspection PyCallByClass,PyTypeChecker,PyArgumentList
        files = QtWidgets.QFileDialog.getOpenFileNames(self, 'Choose %s files' % what,
                                                       self.lastFolder, 'Pilatus data (%s)' % what)[0]
        self.openFiles(files)

    def openFiles(self, files):
        if not files:
            return

        files.sort()
        self.lastFolder = os.path.dirname(files[0])
        self.fileList.addItems(files)
        self.label.setText('Selected files: %d' % self.fileList.count())

    @QtCore.pyqtSlot()
    def delItems(self):
        for item in self.fileList.selectedItems():
            sip.delete(item)
        self.label.setText('Selected files: %d' % self.fileList.count())

    @QtCore.pyqtSlot()
    def clearItems(self):
        self.fileList.clear()
        self.label.setText('Selected files: %d' % self.fileList.count())

    def validatePage(self):
        settings = QtCore.QSettings()
        settings.setValue('Convert/lastFolder', self.lastFolder)
        return Page.validatePage(self)


class OptionsPage(Page):
    # noinspection PyUnresolvedReferences
    def setupUi(self):
        self.cbf = QtGui.QRadioButton('cbf')
        self.cbf.setChecked(True)
        self.edf = QtGui.QRadioButton('edf')

        hrlayout = QtGui.QHBoxLayout()
        vrlayout1 = QtGui.QVBoxLayout()
        vrlayout1.addWidget(self.cbf)
        vrlayout2 = QtGui.QVBoxLayout()
        vrlayout2.addWidget(self.edf)
        hrlayout.addLayout(vrlayout1)
        hrlayout.addLayout(vrlayout2)

        radiosGroupBox = QtGui.QGroupBox('Choose the format to convert')
        radiosGroupBox.setLayout(hrlayout)

        self.binningCheckBox = QtGui.QCheckBox('Make binning')
        self.binningEveryRadio = QtGui.QRadioButton('for every')
        self.binningSpinBox = QtGui.QSpinBox()
        self.binningSpinBox.setDisabled(True)
        self.binningSpinBox.setMinimum(2)
        self.binningSpinBox.setMaximum(65535)
        self.binningPeriodRadio = QtGui.QRadioButton('periodically')
        filesLabel = QtGui.QLabel('files')
        self.binningGroup = QtGui.QButtonGroup()
        self.binningGroup.addButton(self.binningEveryRadio)
        self.binningGroup.addButton(self.binningPeriodRadio)

        def toggleBinning(enable=None):
            if enable is None:
                enable = self.binningCheckBox.isChecked()
            self.binningSpinBox.setEnabled(enable)
            self.binningEveryRadio.setEnabled(enable)
            self.binningPeriodRadio.setEnabled(enable)
            filesLabel.setEnabled(enable)

        toggleBinning(False)
        self.binningEveryRadio.setChecked(True)
        self.binningCheckBox.toggled.connect(toggleBinning)
        self.binningPeriodRadio.toggled.connect(
            lambda: self.binningSpinBox.setDisabled(self.binningPeriodRadio.isChecked())
        )

        hlayout1 = QtGui.QHBoxLayout()
        hlayout1.addWidget(self.binningCheckBox)
        hlayout1.addWidget(self.binningEveryRadio)
        hlayout1.addWidget(self.binningSpinBox)
        hlayout1.addWidget(filesLabel)
        hlayout1.addWidget(self.binningPeriodRadio)
        hlayout1.addStretch()

        self.negativeCheckBox = QtGui.QCheckBox('Set negative intensity as')
        self.negativeSpinBox = QtGui.QSpinBox()
        self.negativeSpinBox.setMinimum(-2)
        self.negativeSpinBox.setDisabled(True)
        self.negativeCheckBox.clicked.connect(
            lambda: self.negativeSpinBox.setEnabled(self.negativeCheckBox.isChecked())
        )

        hlayout2 = QtGui.QHBoxLayout()
        hlayout2.addWidget(self.negativeCheckBox)
        hlayout2.addWidget(self.negativeSpinBox)
        hlayout2.addStretch()

        self.moveAngleCheckBox = QtGui.QCheckBox('Move angle:')
        self.startingAngleSpinBox = QtGui.QDoubleSpinBox()
        self.startingAngleSpinBox.setDecimals(4)
        self.startingAngleSpinBox.setMinimum(-360)
        self.startingAngleSpinBox.setMaximum(360)
        self.angleIncrementSpinBox = QtGui.QDoubleSpinBox()
        self.angleIncrementSpinBox.setDecimals(4)
        self.angleIncrementSpinBox.setMinimum(-360)
        self.angleIncrementSpinBox.setMaximum(360)
        startLabel = QtGui.QLabel('start')
        incLabel = QtGui.QLabel('increment')
        hlayout3 = QtGui.QHBoxLayout()
        hlayout3.addWidget(self.moveAngleCheckBox)
        hlayout3.addWidget(startLabel)
        hlayout3.addWidget(self.startingAngleSpinBox)
        hlayout3.addWidget(incLabel)
        hlayout3.addWidget(self.angleIncrementSpinBox)
        hlayout3.addStretch()

        def showAngle(show):
            self.moveAngleCheckBox.setVisible(show)
            self.startingAngleSpinBox.setVisible(show)
            self.angleIncrementSpinBox.setVisible(show)
            startLabel.setVisible(show)
            incLabel.setVisible(show)

        showAngle(True)
        self.cbf.toggled[bool].connect(showAngle)

        def enableAngle(en):
            self.angleIncrementSpinBox.setEnabled(en)
            self.startingAngleSpinBox.setEnabled(en)

        enableAngle(False)
        self.moveAngleCheckBox.toggled[bool].connect(enableAngle)

        self.int32 = QtGui.QRadioButton('Int32 (for fit2d)')
        self.int32.setChecked(True)
        self.int16 = QtGui.QRadioButton('Int16')
        self.intGroup = QtGui.QButtonGroup()
        self.intGroup.addButton(self.int32)
        self.intGroup.addButton(self.int16)
        self.flipCheckBox = QtGui.QCheckBox('Flip image (for fit2d)')
        self.flipCheckBox.setChecked(True)
        self.addHeaderCheckBox = QtGui.QCheckBox('Add edf header (for fit2d)')
        self.addHeaderCheckBox.setChecked(True)
        hlayout4 = QtGui.QHBoxLayout()
        hlayout4.addWidget(self.int32)
        hlayout4.addWidget(self.int16)
        hlayout4.addStretch()
        hlayout5 = QtGui.QHBoxLayout()
        hlayout5.addWidget(self.flipCheckBox)
        hlayout5.addStretch()
        hlayout6 = QtGui.QHBoxLayout()
        hlayout6.addWidget(self.addHeaderCheckBox)
        hlayout6.addStretch()

        def showEdfOpts(show):
            self.int16.setVisible(show)
            self.int32.setVisible(show)
            self.flipCheckBox.setVisible(show)
            self.addHeaderCheckBox.setVisible(show)

        showEdfOpts(False)
        self.edf.toggled[bool].connect(showEdfOpts)

        vlayout1 = QtGui.QVBoxLayout()
        vlayout1.addLayout(hlayout1)
        vlayout1.addLayout(hlayout2)
        vlayout1.addLayout(hlayout3)
        vlayout1.addLayout(hlayout4)
        vlayout1.addLayout(hlayout5)
        vlayout1.addLayout(hlayout6)

        optionsGroupBox = QtGui.QGroupBox('Options')
        optionsGroupBox.setLayout(vlayout1)

        vlayout2 = QtGui.QVBoxLayout()
        vlayout2.addWidget(radiosGroupBox)
        vlayout2.addWidget(optionsGroupBox)
        self.setLayout(vlayout2)

    def initializePage(self):
        settings = QtCore.QSettings()
        self.setRadio(settings.value('Convert/format', 'cbf'), 'edf', 'cbf')
        binning = pyqt2bool(settings.value('Convert/binning', False))
        self.binningCheckBox.setChecked(binning)
        self.binningSpinBox.setValue(int(settings.value('Convert/binning_value', 1)))
        self.setRadio(settings.value('Convert/bintype', 'binningEveryRadio'), 'binningEveryRadio', 'binningPeriodRadio')
        negative = pyqt2bool(settings.value('Convert/negative', False))
        self.negativeCheckBox.setChecked(negative)
        self.negativeSpinBox.setEnabled(negative)
        self.negativeSpinBox.setValue(int(settings.value('Convert/negative_value', 0)))
        self.angleIncrementSpinBox.setValue(float(settings.value('Convert/angleIncrement', 0)))
        self.startingAngleSpinBox.setValue(float(settings.value('Convert/startingAngle', 0)))
        self.flipCheckBox.setChecked(pyqt2bool(settings.value('Convert/edfFlip', True)))
        self.setRadio(settings.value('Convert/edfInt', 'int32'), 'int16', 'int32')
        self.addHeaderCheckBox.setChecked(pyqt2bool(settings.value('Convert/edfAddHeader', True)))

    def getRadio(self, *radios):
        for item in radios:
            if self.__dict__[item].isChecked():
                return item

    def setRadio(self, value, *radios):
        for item in radios:
            if value == item:
                self.__dict__[item].setChecked(True)
                return

    def validatePage(self):
        settings = QtCore.QSettings()
        settings.setValue('Convert/format', self.getRadio('cbf', 'edf'))
        settings.setValue('Convert/binning', self.binningCheckBox.isChecked())
        settings.setValue('Convert/bintype', self.getRadio('binningEveryRadio', 'binningPeriodRadio'))
        settings.setValue('Convert/binning_value', self.binningSpinBox.value())
        settings.setValue('Convert/negative', self.negativeCheckBox.isChecked())
        settings.setValue('Convert/negative_value', self.negativeSpinBox.value())
        settings.setValue('Convert/startingAngle', self.startingAngleSpinBox.value())
        settings.setValue('Convert/angleIncrement', self.angleIncrementSpinBox.value())
        settings.setValue('Convert/edfInt', self.getRadio('int16', 'int32'))
        settings.setValue('Convert/edfFlip', self.flipCheckBox.isChecked())
        settings.setValue('Convert/edfAddHeader', self.addHeaderCheckBox.isChecked())
        return Page.validatePage(self)


class ConvertPage(Page):
    def setupUi(self):
        self.progress = QtWidgets.QProgressBar()
        self.progress.setMaximum(100)
        self.log = QtWidgets.QListWidget()

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.progress)
        layout.addWidget(self.log)
        self.setLayout(layout)

    def isComplete(self):
        return self.wizard().stopped


class ConvertWizard(QtWidgets.QWizard):
    terminateSignal = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        QtWidgets.QWizard.__init__(self, parent)
        self.addPage(FilesPage())
        self.addPage(OptionsPage())
        self.addPage(ConvertPage())
        self.setWindowTitle('Pylatus image converter')
        self.setOptions(QtWidgets.QWizard.NoBackButtonOnLastPage)
        self.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        matrix = QtGui.QTransform().rotate(-90)
        pixmap = QtGui.QPixmap(':/snbl').scaled(281, 151, QtCore.Qt.KeepAspectRatio,
                                                QtCore.Qt.SmoothTransformation).transformed(matrix)
        self.setPixmap(QtWidgets.QWizard.WatermarkPixmap, pixmap)
        self.loadSettings()
        self.setWindowIcon(QtGui.QIcon(':/convert'))
        # noinspection PyUnresolvedReferences
        self.currentIdChanged[int].connect(self.checkPage)
        self.stopped = False
        self.workerThread = QtCore.QThread()
        # noinspection PyUnresolvedReferences
        self.rejected.connect(self.terminate)

    def terminate(self):
        self.terminateSignal.emit()
        self.finished()

    def checkPage(self, page):
        if page == 2:
            self.convert()

    def closeEvent(self, event):
        self.saveSettings()
        event.accept()

    def loadSettings(self):
        settings = QtCore.QSettings()
        self.restoreGeometry(settings.value('Convert/Geometry', QtCore.QByteArray()))

    def saveSettings(self):
        settings = QtCore.QSettings()
        settings.setValue('Convert/Geometry', self.saveGeometry())

    def showProgress(self, images, converted, queueLength):
        self.log.addItem(images)
        self.log.scrollToBottom()
        self.progress.setValue(100.0 * converted / queueLength)
        if converted == queueLength:
            self.finished()

    def finished(self, p_int=0):
        self.stopped = True
        if hasattr(self, 'page2'):
            self.page2.completeChanged.emit()
        self.workerThread.quit()
        self.workerThread.wait()

    def convert(self):
        self.page2 = self.page(2)
        self.progress = self.page2.progress
        self.log = self.page2.log

        fileList = self.page(0).fileList
        count = fileList.count()

        page1 = self.page(1)
        if page1.negativeCheckBox.isChecked():
            negative = page1.negativeSpinBox.value()
        else:
            negative = NEGATIVE_THRESHOLD

        self.format = page1.getRadio('cbf', 'edf')
        if page1.moveAngleCheckBox.isChecked():
            move = [page1.startingAngleSpinBox.value(), page1.angleIncrementSpinBox.value()]
        else:
            move = []
        images = [fileList.item(i).text() for i in range(count)]

        opts = {
            'images': images,
            'format': self.format,
            'negative': negative,
            'binning': page1.binningCheckBox.isChecked(),
            'bintype': page1.binningSpinBox.value() if page1.binningSpinBox.isEnabled() else 0,
            'move': move,
            'edfInt': page1.getRadio('int16', 'int32'),
            'edfFlip': page1.flipCheckBox.isChecked(),
            'edfHeader': page1.addHeaderCheckBox.isChecked(),
        }
        self.worker = QCbfConvert(copy.deepcopy(opts))
        self.worker.moveToThread(self.workerThread)
        # noinspection PyUnresolvedReferences
        self.workerThread.started.connect(self.worker.convert)
        self.worker.progressSignal.connect(self.showProgress)
        self.terminateSignal.connect(self.worker.terminateAll)
        self.workerThread.start()
