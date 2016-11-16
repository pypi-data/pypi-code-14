#!/usr/bin/env python
# -*- coding: utf-8 -*-

import binascii
import cryio


class Background:
    def __init__(self):
        self._bkg = None
        self._bkg_checksum = 0
        self._bkg_coef = 1

    def init(self, files, dark=None, normalize=None, coefficient=1, flatfield=None):
        if files:
            checksum = binascii.crc32(''.join(files).encode())
            res = checksum == self._bkg_checksum
            self._bkg_checksum = checksum
            if res and self._bkg_coef == coefficient:
                return
            self._bkg = cryio.openImage(files[0])
            self._bkg.float()
            if dark:
                self._bkg = dark(self._bkg)
            if normalize:
                normalize(self._bkg)
            for image in files[1:]:
                bkg = cryio.openImage(image)
                if dark:
                    bkg = dark(bkg.float())
                if normalize:
                    bkg = normalize(bkg)
                self._bkg.array += bkg.array
                self._bkg.transmission += bkg.transmission
            if flatfield:
                self._bkg = flatfield(self._bkg)
            self._bkg.array *= coefficient / len(files)
            self._bkg.transmission /= len(files)
            self._bkg_coef = coefficient
        else:
            self._bkg = None
            self._bkg_checksum = 0
            self._bkg_coef = 1

    def __call__(self, image, transmission=False, thickness=1, concentration=0):
        image.transmission_coefficient = 0
        if self._bkg is not None:
            if transmission and image.transmission and self._bkg.transmission:
                image.array = (image.array - self._bkg.array * image.transmission * (1 - concentration) /
                               self._bkg.transmission) / image.transmission / thickness
                image.transmission_coefficient = image.transmission / self._bkg.transmission
            else:
                image.array -= self._bkg.array
        return image
