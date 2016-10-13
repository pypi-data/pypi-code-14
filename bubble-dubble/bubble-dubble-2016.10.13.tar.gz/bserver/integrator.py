#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import time
import traceback
import numpy as np
from decor import floodfield, darkcurrent, distortion, background
from integracio import igracio
from ..bcommon import corrections, compressor


class Integrator:
    def __init__(self):
        self._i = igracio.IGracio()
        self.normalize = corrections.normalization.Normalization()
        self.mask = corrections.mask.Mask()
        self.background = background.Background()
        self.darkSample = darkcurrent.DarkCurrent()
        self.darkBackground = darkcurrent.DarkCurrent()
        self.flatfield = floodfield.FloodField()
        self.distortion = distortion.Distortion()

    def adjustCorrections(self, interface):
        self.interface = interface
        self._i.poni = self.interface.poni
        self._i.azimuth = self.interface.azimuth
        self._i.units = self.interface.units
        if self.interface.detector == 'Frelon':
            self.darkSample.init(self.interface.darkSample)
            self.darkBackground.init(self.interface.darkBackground)
            self.flatfield.init(self.interface.flood)
            self.distortion.init(self.interface.spline)
        else:
            self.darkSample.init(None)
            self.darkBackground.init(None)
            self.flatfield.init(None)
            self.distortion.init(None)
        self.normalize.beamline = self.interface.beamline
        self.mask.init(self.interface.maskFile, self.interface.beamline, self.interface.type)
        self.background.init(self.interface.backgroundFiles, self.darkBackground, self.normalize,
                             self.interface.bkgCoef, self.flatfield)

    def __call__(self, filename, image, interface, catchException=True):
        self.adjustCorrections(interface)
        if catchException:
            # noinspection PyBroadException
            try:
                result = self._integrate(filename, image)
            except:
                traceback.print_exc(file=sys.stdout)
                print('Frame: {}'.format(filename))
                return None
            else:
                return result
        else:
            return self._integrate(filename, image)

    def _integrate(self, filename, frames):
        retval = None
        ext = self.interface.ext
        if ext.startswith('.'):
            ext = ext[1:]
        if frames.header.get('Bubble_normalized', 0):
            return retval
        path, base = os.path.split(filename)
        newpath = os.path.join(path, self.interface.subdir)
        if frames.multiframe:
            newpath = os.path.join(newpath, base[:-4])
        try:  # it seems that here we can have race conditions
            os.makedirs(newpath)
        except OSError:
            pass
        for i, image in enumerate(frames):
            chifile = os.path.join(newpath, '{}{}.{}'.format(base[:-4], '_{:05d}'.format(i) if image.multiframe else '',
                                                             ext if ext else 'dat'))
            image.float()
            self.darkSample(image)
            self.flatfield(image)
            self.normalize(image)
            self.background(image, self.interface.calcTransmission, self.interface.thickness,
                            self.interface.concentration)
            image.array *= self.interface.calibration
            self.mask(image)
            self.distortion(image)
            res = self._i(image.array)
            self.writeChiFile(chifile, res)
            self.writeTransmission(chifile, image.transmission_coefficient)
            self.saveNormalizedFrame(chifile, image)
            res_data = res_img = None
            if not self.interface.speed:
                res_img = corrections.beamline.correctImage(self.interface.beamline, self.interface.type, image.array)
                res_img = compressor.compressNumpyArray(res_img)
                res_data = [compressor.compressNumpyArray(array) for array in res]

            if self.interface.sspeed:
                self.interface.speedcounter += 1
            retval = {
                'imageFile': filename,
                'chiFile': chifile,
                'transmission': image.transmission_coefficient,
                'data1d': res_data,
                'image': res_img,
                'timestamp': time.time(),
                'sent': False,
            }
        return retval

    def writeChiFile(self, chifile, res):
        np.savetxt(chifile, np.array(res).T, '%.6e')

    def saveNormalizedFrame(self, chifile, image):
        if self.interface.save:
            image.array = image.array.astype(np.int32)
            name = '{}_norm.edf'.format(chifile[:-4])
            image.save_edf(name, Bubble_normalized=1)

    def writeTransmission(self, chifile, transCoef):
        if self.interface.calcTransmission:
            with open(chifile, 'r+') as chi:
                old = chi.read()
                chi.seek(0)
                chi.write('# Transmission coefficient {0:.7f}\n{1}'.format(transCoef, old))
