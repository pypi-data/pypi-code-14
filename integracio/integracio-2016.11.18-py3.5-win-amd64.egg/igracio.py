#!/usr/bin/env python
# -*- coding: utf-8 -*-

import binascii
import threading
import numpy as np
from . import _cgracio, poni


class IGracio:
    __units = {'t': 0, 'q': 1}

    def __init__(self):
        self._i = None
        self._poni = None
        self._poni_checksum = 0
        self._units = 't'
        self._azimuth = 0, 0
        self.__lock = threading.Lock()
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
            self._i = None

    def _initialization(self, shape):
        with self.__lock:
            if (self.dim1, self.dim2) != shape:
                self.dim1, self.dim2 = shape
                self._i = None
            if not self._i and self._poni:
                self._i = _cgracio.init()
                self._poni.units = self.__units.get(self._units, 0)
                buf = _cgracio.calc_pos(self._i, self.dim1, self.dim2, self._poni.geometry())
                self.pos = np.frombuffer(buf, np.float32)

    def _integrate(self, image):
        self._initialization(image.shape)
        img = np.ascontiguousarray(image, np.float32).tobytes()
        bufs = _cgracio.integrate(self._i, img, *self._azimuth)
        return self.pos, np.frombuffer(bufs[0], np.float32), np.frombuffer(bufs[1], np.float32)

    def __call__(self, image):
        return self._integrate(image)

    @property
    def units(self):
        return self._units

    @units.setter
    def units(self, units):
        if units != self._units:
            self._units = units
            self._i = None

    @property
    def azimuth(self):
        return self._azimuth

    @azimuth.setter
    def azimuth(self, azimuth):
        if self._azimuth != azimuth:
            if azimuth is None:
                azimuth = 0, 0
            self._azimuth = azimuth
