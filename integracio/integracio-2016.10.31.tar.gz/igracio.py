#!/usr/bin/env python
# -*- coding: utf-8 -*-

import binascii
import numpy as np
# noinspection PyUnresolvedReferences
from . import _cgracio, poni


class IGracio:
    __units = {'t': 0, 'q': 1}

    def __init__(self):
        self._i = _cgracio.init()
        self._poni = None
        self._poni_checksum = 0
        self._units = 't'
        self._azimuth = 0, 0
        self.__internal_corners = 0
        self._initialized = False
        self.dim1 = 0
        self.dim2 = 0

    def _check_poni_checksum(self, poni_text):
        checksum = binascii.crc32(poni_text.encode())
        res = checksum == self._poni_checksum
        self._poni_checksum = checksum
        return res

    @property
    def poni(self):
        return self._poni

    @poni.setter
    def poni(self, poni_text):
        if not self._check_poni_checksum(poni_text):
            self._poni = poni.Poni(poni_text)
            self._initialized = False

    def _initialization(self, shape):
        if (self.dim1, self.dim2) != shape:
            self.dim1, self.dim2 = shape
            self._initialized = False
        if not self._initialized and self._poni:
            self._poni.units = self.__units.get(self._units, 0)
            self._poni.internal_corners = self._internal_corners
            bufs = _cgracio.calc_pos(self._i, self.dim1, self.dim2, self._poni.geometry())
            if isinstance(bufs, tuple):
                tth, dtth, chi, dchi = bufs
                dtth = self._calc_dtth(tth, dtth)
                dchi = self._calc_dchi(chi, dchi)
                bufs = _cgracio.calc_bins(self._i, dtth, dchi)
            self.pos = np.frombuffer(bufs, np.float64)
            self._initialized = True

    def _calc_dtth(self, tth, dtth):
        tth = np.frombuffer(tth, np.float64).reshape((self.dim1, self.dim2))
        tth_corner = np.frombuffer(dtth, np.float64).reshape((self.dim1 + 1, self.dim2 + 1))
        delta = np.zeros((self.dim1, self.dim2, 4), dtype=np.float64)
        delta[:, :, 0] = abs(tth_corner[:-1, :-1] - tth)
        delta[:, :, 1] = abs(tth_corner[1:, :-1] - tth)
        delta[:, :, 2] = abs(tth_corner[1:, 1:] - tth)
        delta[:, :, 3] = abs(tth_corner[:-1, 1:] - tth)
        return delta.max(axis=2).tostring()

    def _calc_dchi(self, chi, dchi):
        pi2 = np.pi * 2
        chi = np.frombuffer(chi, np.float64).reshape((self.dim1, self.dim2))
        chi_corner = np.frombuffer(dchi, np.float64).reshape((self.dim1 + 1, self.dim2 + 1))
        delta = np.zeros((self.dim1, self.dim2, 4), dtype=np.float64)
        delta[:, :, 0] = np.minimum(((chi_corner[:-1, :-1] - chi) % pi2), ((chi - chi_corner[:-1, :-1]) % pi2))
        delta[:, :, 1] = np.minimum(((chi_corner[1:, :-1] - chi) % pi2), ((chi - chi_corner[1:, :-1]) % pi2))
        delta[:, :, 2] = np.minimum(((chi_corner[1:, 1:] - chi) % pi2), ((chi - chi_corner[1:, 1:]) % pi2))
        delta[:, :, 3] = np.minimum(((chi_corner[:-1, 1:] - chi) % pi2), ((chi - chi_corner[:-1, 1:]) % pi2))
        return delta.max(axis=2).tostring()

    def _integrate(self, image):
        self._initialization(image.shape)
        img = image.astype(np.float64).tostring()
        bufs = _cgracio.integrate(self._i, img, *self._azimuth)
        return self.pos, np.frombuffer(bufs[0], np.float64), np.frombuffer(bufs[1], np.float64)

    def __call__(self, image):
        return self._integrate(image)

    @property
    def units(self):
        return self._units

    @units.setter
    def units(self, units):
        if units != self._units:
            self._units = units
            self._initialized = False

    @property
    def azimuth(self):
        return self._azimuth

    @azimuth.setter
    def azimuth(self, azimuth):
        if self._azimuth != azimuth:
            if azimuth is None:
                azimuth = 0, 0
            self._azimuth = azimuth

    def positions(self):
        return [np.frombuffer(b, np.float64).reshape((self.dim1, self.dim2)) for b in _cgracio.get_pos(self._i)]

    @property
    def _internal_corners(self):
        return self.__internal_corners

    @_internal_corners.setter
    def _internal_corners(self, value):
        self.__internal_corners = value
