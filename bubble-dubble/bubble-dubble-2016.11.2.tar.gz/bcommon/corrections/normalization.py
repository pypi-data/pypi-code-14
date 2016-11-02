#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Normalization:
    def __init__(self):
        self._beamline = None

    @property
    def beamline(self):
        return self._beamline

    @beamline.setter
    def beamline(self, beamline):
        self._beamline = beamline

    def __call__(self, img):
        try:
            return {
                'Dubble': self._dubble_normalization,
                'SNBL': self._snbl_normalization,
            }[self._beamline](img)
        except KeyError:
            return img

    def _dubble_normalization(self, img):
        i1 = img.header.get('Monitor', 0)
        photo = img.header.get('Photo', 0)
        img.float()
        if i1 < 1:
            i1 = img.array.sum()
        if i1 > 1:
            img.array /= i1
            if photo:
                img.transmission = photo / i1
        return img

    def _snbl_normalization(self, img, flux=None):
        img.float()
        flux = img.header.get('Flux') or flux
        if flux:
            img.array /= flux
        return img
