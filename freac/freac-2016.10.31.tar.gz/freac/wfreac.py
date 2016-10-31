#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import glob
from datetime import datetime
import collections
import numpy as np
from PyQt5 import QtGui, QtCore, QtWidgets
import cryio
from cryio import crysalis, esperanto
from decor import darkcurrent, distortion, floodfield
from freac.ui.qfreac import Ui_QFreac
from freac import pyqt2bool as _


FRELON_CENTER = 1024
FRELON_PIXEL = 0.0475


class FreacWorker(QtCore.QObject):
    progressSignal = QtCore.pyqtSignal(int, str)
    finishedSignal = QtCore.pyqtSignal(list)
    OMEGA_TOLERANCE = 1e-4
    OMEGA_ZERO = -165

    def __init__(self):
        QtCore.QObject.__init__(self)
        self.errors = []
        self.opts = {}
        self.stop = True
        self.nscans = 0
        self.flood = floodfield.FloodField()
        self.dark = darkcurrent.DarkCurrent()
        self.dist = distortion.Distortion()

    def stopIt(self):
        self.stop = True

    def checkDirs(self):
        if not os.path.isdir(self.opts['dir']):
            self.errors.append('The base directory cannot be found!')
            self.finish()
            return False
        try:
            edna = os.path.join(self.opts['dir'], '..', '{}_edna'.format(self.opts['dir']))
            if not os.path.exists(edna):
                os.mkdir(edna)
            self.outdir = os.path.join(edna, 'crysalis')
            if not os.path.exists(self.outdir):
                os.mkdir(self.outdir)
            self.basename = os.path.basename(self.opts['dir'])
        except IOError:
            self.errors.append('Cannot create output directory')
            self.finish()
            return False
        return True

    def finish(self):
        self.stopIt()
        self.finishedSignal.emit(self.errors)

    def quit(self):
        self.stopIt()
        self.thread().quit()

    def init_distortion(self):
        try:
            self.dark.init([self.opts['dark']])
        except cryio.ImageError:
            self.errors.append('Dark file "{}" does not exist or it is corrupted. '
                               'Correction was not applied!'.format(self.opts['dark']))
        try:
            self.flood.init(self.opts['flood'])
        except cryio.ImageError:
            self.errors.append('Dark file "{}" does not exist or it is corrupted. '
                               'Correction was not applied!'.format(self.opts['flood']))
        try:
            self.dist.init(self.opts['spline'])
        except IOError:
            self.errors.append('Spline file was not found! Correction was not applied!')

    def apply_distortion(self, image):
        image.float()
        image = self.dist(self.flood(self.dark(image)))
        image.array = image.array.astype(np.int32)
        return image

    def run(self, opts):
        self.stop = False
        self.opts = opts
        self.errors = []
        if not self.checkDirs():
            return
        self.init_distortion()
        if not self.convertEDF():
            return
        # if not self.checkMultipleOmega():
        #     return
        self.createCrysalis()
        self.finish()

    def convertEDF(self):
        self.esp = esperanto.EsperantoImage()
        self.scans = collections.OrderedDict()
        edfs = sorted(glob.glob(os.path.join(self.opts['dir'], '*.edf')), reverse=True)
        nedfs = len(edfs)
        old_phi = None
        run = 1
        num = 0
        for i, fedf in enumerate(edfs, 1):
            # noinspection PyArgumentList
            QtCore.QCoreApplication.processEvents()
            if self.stop:
                self.finish()
                return False
            self.progressSignal.emit(int(100.0 * i / nedfs), 'Converting {}'.format(os.path.basename(fedf)))
            edf = cryio.openImage(fedf)
            phi = edf.header.get('hphi', 0)
            if self.opts['phi']:
                for p in self.opts['phi']:
                    if p - 1 <= phi <= p + 1:
                        break
                else:
                    continue
            if old_phi is None:
                run = 1
                num = 0
                old_phi = phi
            elif old_phi != phi:
                run += 1
                old_phi = phi
                num = 0
            num += 1
            if phi not in self.scans:
                step = self.opts['Angle_increment'] or edf.header.get('OmegaStep', 1)
                # omega = -edf.header.get('Omega', 0) - self.opts['Start_angle']
                self.scans[phi] = [{
                    'files': [],
                    'nfiles': [],
                    'count': 0,
                    'omegas': [],
                    'Oscillation_axis': 'OMEGA',
                    'Phi': phi,
                    'Phi_increment': 0,
                    'Start_angle': self.opts['Start_angle'],
                    'Angle_increment': step,
                    'Omega': self.opts['Start_angle'],
                    'Omega_increment': step,
                    'Kappa': self.opts['kappa'],
                    'Detector_distance': self.opts['Detector_distance'] or edf.header.get('nfdtx', 100) * 1e-3,
                    'Real_start_angle': self.opts['Start_angle'],
                    'Wavelength': self.opts['Wavelength'],
                    'pixel_size': self.opts['pixel_size'],
                    'Beam_x': self.opts['Beam_x'],
                    'Beam_y': self.opts['Beam_y'],
                    'Detector_Voffset': 0,
                    'Exposure_time': 1,
                    'Exposure_period': 1,
                    'omega_runs': None,
                    'omega': self.opts['Start_angle'],
                    'theta': 0,
                    'kappa': self.opts['kappa'],
                    'phi': phi,
                    'domega': step,
                    'dtheta': 0,
                    'dkappa': 0,
                    'dphi': 0,
                    'center_x': self.opts['Beam_x'],
                    'center_y': self.opts['Beam_y'],
                    'alpha': 50,
                    'dist': (self.opts['Detector_distance'] or edf.header.get('nfdtx', 0.1)) * 1e3,
                    'l1': self.opts['Wavelength'],
                    'l2': self.opts['Wavelength'],
                    'l12': self.opts['Wavelength'],
                    'b': self.opts['Wavelength'],
                    'mono': 0.98,
                    'monotype': 'SYNCHROTRON',
                    'chip': edf.array.shape,
                }]
            basename = '{}_{:d}_{:d}.esperanto'.format(self.basename, run, num)
            self.scans[phi][0]['files'].append(basename)
            self.scans[phi][0]['nfiles'].append(basename)
            self.scans[phi][0]['count'] += 1
            edf = self.apply_distortion(edf)
            self.esp.save(os.path.join(self.outdir, basename), edf.array, **self.scans[phi][0])
            self.scans[phi][0]['omegas'].append(edf.header.get('Omega'))
            self.scans[phi][0]['Start_angle'] += self.scans[phi][0]['Angle_increment']
            self.scans[phi][0]['Omega'] = self.scans[phi][0]['Start_angle']
            self.scans[phi][0]['omega'] = self.scans[phi][0]['Start_angle']
        self.nscans = run
        return True

    def checkMultipleOmega(self):
        self.nscans = 0
        for phi in self.scans:
            sa = self.scans[phi][0]['Real_start_angle']
            ai = self.scans[phi][0]['Angle_increment']
            aincm = ai - self.OMEGA_TOLERANCE
            aincp = ai + self.OMEGA_TOLERANCE
            omega_runs, omegas = [], []
            omega_runs.append(omegas)
            for o1, o2 in zip(self.scans[phi][0]['omegas'][:-1], self.scans[phi][0]['omegas'][1:]):
                if o1 is not None and o2 is not None and not aincm <= abs(o1 - o2) <= aincp:
                    omegas.append(o1)
                    omegas = []
                    omega_runs.append(omegas)
                    continue
                omegas.append(o1)
            omegas.append(self.scans[phi][0]['omegas'][-1])
            if len(omega_runs) > 1:
                omega_runs.sort()
                scan = self.scans[phi][0]
                self.scans[phi] = []
                first, diff = omega_runs[0][0], 0
                for i, omega_run in enumerate(omega_runs):
                    scan['count'] = len(omega_run)
                    scan['nfiles'] = [scan['files'][scan['omegas'].index(o)] for o in omega_run]
                    j = 0
                    for f, jo in zip(scan['nfiles'], enumerate(omega_run)):
                        f1 = os.path.join(self.outdir, f)
                        h = cryio.cbfimage.CbfHeader(f1)
                        j, o = jo
                        if i and not j:
                            diff = omega_run[j] - first
                        h.header['Omega'] = h.header['Start_angle'] = diff + sa + ai * j
                        h.header['pixel_size'] = self.opts['pixel_size']
                        h.save_cbf(f1)
                        self.progressSignal.emit(int(100.0 * j / len(omega_run)), 'Finalizing {}'.format(f))
                        # noinspection PyArgumentList
                        QtCore.QCoreApplication.processEvents()
                        if self.stop:
                            self.finish()
                            return False
                    scan['Real_start_angle'] = diff + sa
                    scan['Start_angle'] = diff + sa + ai * (j + 1)
                    self.scans[phi].append(scan.copy())
                    self.nscans += 1
            else:
                self.nscans += 1
        self.progressSignal.emit(100, 'Finished {}'.format(os.path.basename(self.opts['dir'])))
        return True

    def createCrysalis(self):
        runHeader = crysalis.RunHeader(self.basename.encode(), self.outdir.encode(), self.nscans)
        runname = os.path.join(self.outdir, self.basename)
        runFile = []
        i = 0
        shape = None
        for phi in self.scans:
            for omega_run in self.scans[phi]:
                dscr = crysalis.RunDscr(i)
                dscr.axis = crysalis.SCAN_AXIS[omega_run['Oscillation_axis']]
                dscr.kappa = omega_run['Kappa']
                dscr.omegaphi = phi
                dscr.start = omega_run['Real_start_angle']
                dscr.end = omega_run['Start_angle'] - omega_run['Angle_increment']
                dscr.width = omega_run['Angle_increment']
                dscr.todo = dscr.done = omega_run['count']
                dscr.exposure = omega_run['Exposure_time']
                runFile.append(dscr)
                i += 1
                shape = omega_run['chip'][0]
        crysalis.saveRun(runname, runHeader, runFile)
        crysalis.saveSet(runname, 'Frelon')
        crysalis.saveCcd(runname, 'esperanto')
        crysalis.saveSel(runname, 'esperanto')
        crysalis.savePar(runname, {'wavelength': self.opts['Wavelength'], 'path': self.outdir,
                                   'center_y': self.opts['Beam_y'], 'center_x': self.opts['Beam_x'],
                                   'basename': self.basename, 'dist': self.opts['Detector_distance'] * 1e3,
                                   'date': datetime.now().strftime(u'%Y-%m-%d %H:%M:%S'), 'chip': True,
                                   'chip1': shape, 'chip2': shape, })
        crysalis.saveCrysalisExpSettings(self.outdir)


class WFreac(QtWidgets.QDialog, Ui_QFreac):
    stopWorkerSignal = QtCore.pyqtSignal()
    runWorkerSignal = QtCore.pyqtSignal(dict)
    quitWorkerSignal = QtCore.pyqtSignal()

    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.setupUi(self)
        v = QtGui.QDoubleValidator()
        self.phiEdit.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp('^[\d ]*$')))
        self.llambdaEdit.setValidator(v)
        self.kappaEdit.setValidator(v)
        self.omegaEdit.setValidator(v)
        self.dOmegaEdit.setValidator(v)
        self.distEdit.setValidator(v)
        self.pixEdit.setValidator(v)
        self.x0Edit.setValidator(v)
        self.y0Edit.setValidator(v)
        self.stopButton.setVisible(False)
        self.loadSettings()
        self.workerThread = QtCore.QThread()
        self.worker = FreacWorker()
        self.worker.moveToThread(self.workerThread)
        self.worker.progressSignal.connect(self.showProgress)
        self.worker.finishedSignal.connect(self.workerFinished)
        self.stopWorkerSignal.connect(self.worker.stopIt)
        self.runWorkerSignal.connect(self.worker.run)
        self.quitWorkerSignal.connect(self.worker.quit)

    def saveSettings(self):
        s = QtCore.QSettings()
        s.setValue('WFreac/Geometry', self.saveGeometry())
        s.setValue('WFreac/lambda', self.llambdaEdit.text())
        s.setValue('WFreac/phi', self.phiEdit.text())
        s.setValue('WFreac/kappa', self.kappaEdit.text())
        s.setValue('WFreac/omega', self.omegaEdit.text())
        s.setValue('WFreac/domega', self.dOmegaEdit.text())
        s.setValue('WFreac/dist', self.distEdit.text())
        s.setValue('WFreac/pix', self.pixEdit.text())
        s.setValue('WFreac/y0', self.y0Edit.text())
        s.setValue('WFreac/x0', self.x0Edit.text())
        s.setValue('WFreac/lastdir', self.lastdir)
        s.setValue('WFreac/dir', self.dirEdit.text())
        s.setValue('WFreac/dark', self.darkEdit.text())
        s.setValue('WFreac/flood', self.floodEdit.text())
        s.setValue('WFreac/spline', self.splineEdit.text())
        s.setValue('WFreac/comega', self.omegaCheckBox.isChecked())
        s.setValue('WFreac/cdomega', self.dOmegaCheckBox.isChecked())
        s.setValue('WFreac/cdist', self.distCheckBox.isChecked())
        s.setValue('WFreac/cpix', self.pixCheckBox.isChecked())
        s.setValue('WFreac/cx0', self.x0CheckBox.isChecked())
        s.setValue('WFreac/cy0', self.y0CheckBox.isChecked())

    def loadSettings(self):
        s = QtCore.QSettings()
        self.restoreGeometry(s.value('WFreac/Geometry', QtCore.QByteArray()))
        self.phiEdit.setText(s.value('WFreac/phi', ''))
        self.kappaEdit.setText(s.value('WFreac/kappa', '0'))
        self.llambdaEdit.setText(s.value('WFreac/lambda', '0.4'))
        self.omegaEdit.setText(s.value('WFreac/omega', '0'))
        self.dOmegaEdit.setText(s.value('WFreac/dOmega', '1'))
        self.distEdit.setText(s.value('WFreac/dist', '100'))
        self.pixEdit.setText(s.value('WFreac/pix', '47.5'))
        self.y0Edit.setText(s.value('WFreac/y0', '1024'))
        self.x0Edit.setText(s.value('WFreac/x0', '1024'))
        self.lastdir = s.value('WFreac/lastdir', '')
        self.dirEdit.setText(s.value('WFreac/dir', ''))
        self.darkEdit.setText(s.value('WFreac/dark', ''))
        self.floodEdit.setText(s.value('WFreac/flood', ''))
        self.splineEdit.setText(s.value('WFreac/spline', ''))
        self.omegaCheckBox.setChecked(_(s.value('WFreac/comega')))
        self.dOmegaCheckBox.setChecked(_(s.value('WFreac/cdomega')))
        self.distCheckBox.setChecked(_(s.value('WFreac/cdist')))
        self.pixCheckBox.setChecked(_(s.value('WFreac/cpix')))
        self.x0CheckBox.setChecked(_(s.value('WFreac/cx0')))
        self.y0CheckBox.setChecked(_(s.value('WFreac/cy0')))

    def closeEvent(self, event):
        QtWidgets.QDialog.closeEvent(self, event)
        self.hide()
        self.saveSettings()
        self.quitWorkerSignal.emit()
        self.workerThread.wait()

    def on_omegaCheckBox_toggled(self, checked):
        self.omegaEdit.setEnabled(checked)

    def on_dOmegaCheckBox_toggled(self, checked):
        self.dOmegaEdit.setEnabled(checked)

    def on_distCheckBox_toggled(self, checked):
        self.distEdit.setEnabled(checked)

    def on_pixCheckBox_toggled(self, checked):
        self.pixEdit.setEnabled(checked)

    def on_x0CheckBox_toggled(self, checked):
        self.x0Edit.setEnabled(checked)

    def on_y0CheckBox_toggled(self, checked):
        self.y0Edit.setEnabled(checked)

    @QtCore.pyqtSlot()
    def on_runButton_clicked(self):
        dire = self.dirEdit.text()
        if not dire:
            self.showError(['Directory must be provided!'])
            return
        d = {
            'dir': dire,
            'Wavelength': float(self.llambdaEdit.text() or 0.4),
            'Start_angle': float(self.omegaEdit.text() or 0) if self.omegaCheckBox.isChecked() else -180,
            'Angle_increment': float(self.dOmegaEdit.text() or 0) if self.dOmegaCheckBox.isChecked() else 0,
            'Detector_distance': float(self.distEdit.text() or 0) if self.distCheckBox.isChecked() else 0,
            'pixel_size': float(self.pixEdit.text() or FRELON_PIXEL) if self.pixCheckBox.isChecked() else FRELON_PIXEL,
            'Beam_x': float(self.x0Edit.text() or FRELON_CENTER) if self.x0CheckBox.isChecked() else FRELON_CENTER,
            'Beam_y': float(self.y0Edit.text() or FRELON_CENTER) if self.y0CheckBox.isChecked() else FRELON_CENTER,
            'dark': self.darkEdit.text(),
            'flood': self.floodEdit.text(),
            'spline': self.splineEdit.text(),
            'phi': [float(phi) for phi in self.phiEdit.text().split()],
            'kappa': float(self.kappaEdit.text() or 0),
        }
        d['pixel_size'] *= 1e3
        self.runWorkerSignal.emit(d)
        self.runButton.setVisible(False)
        self.stopButton.setVisible(True)
        self.progressBar.setValue(0)

    @QtCore.pyqtSlot()
    def on_stopButton_clicked(self):
        self.stopWorkerSignal.emit()

    def showEvent(self, event):
        QtWidgets.QDialog.showEvent(self, event)
        self.workerThread.start()

    def showProgress(self, value, text):
        self.progressBar.setFormat('{0}: %p%'.format(text))
        self.progressBar.setValue(value)

    def workerFinished(self, errors):
        self.runButton.setVisible(True)
        self.stopButton.setVisible(False)
        if errors:
            self.showError(errors)

    def showError(self, errors):
        # noinspection PyCallByClass,PyArgumentList,PyTypeChecker
        QtWidgets.QMessageBox.critical(self, 'Freac error', '\n'.join(errors))

    @QtCore.pyqtSlot()
    def on_dirButton_clicked(self):
        # noinspection PyCallByClass,PyTypeChecker,PyArgumentList
        dire = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select directory', self.lastdir)
        if dire:
            self.dirEdit.setText(dire)
            self.lastdir = dire

    @QtCore.pyqtSlot()
    def on_floodButton_clicked(self):
        # noinspection PyCallByClass,PyTypeChecker,PyArgumentList
        fn = QtWidgets.QFileDialog.getOpenFileName(self, 'Choose flood file', self.lastdir, 'EDF (*.edf)')[0]
        if fn:
            self.floodEdit.setText(fn)

    @QtCore.pyqtSlot()
    def on_darkButton_clicked(self):
        # noinspection PyCallByClass,PyTypeChecker,PyArgumentList
        fn = QtWidgets.QFileDialog.getOpenFileName(self, 'Choose dark file', self.lastdir, 'EDF (*.edf)')[0]
        if fn:
            self.darkEdit.setText(fn)

    @QtCore.pyqtSlot()
    def on_splineButton_clicked(self):
        # noinspection PyCallByClass,PyTypeChecker,PyArgumentList
        fn = QtWidgets.QFileDialog.getOpenFileName(self, 'Choose spline file', self.lastdir, 'All files (*.*)')[0]
        if fn:
            self.splineEdit.setText(fn)
