#!/usr/bin/env python
# -*- coding: utf-8 -*-

import binascii
import threading
import numpy as np
from .spline import Spline
from . import _distortion


class Distortion:
    def __init__(self):
        self._lock = threading.Lock()
        self._initialized = False
        self.pos = None
        self.delta0 = None
        self.delta1 = None
        self.spline = None
        self.shape = None
        self.max_size = None
        self.bin_size = None
        self.lut = None
        self._spline_checksum = 0

    def init(self, spline, shape):
        with self._lock:
            if spline:
                checksum = binascii.crc32(spline.encode())
                res = checksum == self._spline_checksum
                self._spline_checksum = checksum
                if not res:
                    self.spline = Spline(spline)
                    self._initialized = False
                if shape != self.shape:
                    self.shape = shape
                    self._initialized = False
            else:
                self._spline_checksum = 0
                self._initialized = True
            if not self._initialized and self.shape:
                self.calc_pos()
                self.calc_size()
                self.calc_lut()

    def __call__(self, image):
        if self._spline_checksum:
            try:
                image.array = self._correct(image.array)
            except AttributeError:
                image = self._correct(image)
        return image

    def _correct(self, image):
        return _distortion.correct_lut(image, self.shape, self.lut)

    def calc_cartesian_positions(self, d1, d2):
        d1c = d1 + 0.5
        d2c = d2 + 0.5
        dx = self.spline.func_x_y(d2c, d1c, 0)
        dy = self.spline.func_x_y(d2c, d1c, 1)
        return dy + d1c, dx + d2c

    def calc_pos(self):
        dim1, dim2 = self.shape
        pos_corners = np.empty((dim1+1, dim2+1, 2), dtype=np.float64)
        d1 = np.outer(np.arange(dim1+1, dtype=np.float64), np.ones(dim2+1, dtype=np.float64)) - 0.5
        d2 = np.outer(np.ones(dim1+1, dtype=np.float64), np.arange(dim2+1, dtype=np.float64)) - 0.5
        pos_corners[:, :, 0], pos_corners[:, :, 1] = self.calc_cartesian_positions(d1, d2)
        pos = np.empty((dim1, dim2, 4, 2), dtype=np.float32)
        pos[:, :, 0, :] = pos_corners[:-1, :-1]
        pos[:, :, 1, :] = pos_corners[:-1, 1:]
        pos[:, :, 2, :] = pos_corners[1:, 1:]
        pos[:, :, 3, :] = pos_corners[1:, :-1]
        self.pos = pos
        self.delta0 = int((np.ceil(pos_corners[1:, :, 0]) - np.floor(pos_corners[:-1, :, 0])).max())
        self.delta1 = int((np.ceil(pos_corners[:, 1:, 1]) - np.floor(pos_corners[:, :-1, 1])).max())

    def calc_size(self):
        self.bin_size = _distortion.calc_size(self.pos, self.shape)
        self.max_size = self.bin_size.max()

    def calc_lut(self):
        self.lut = _distortion.calc_lut(self.pos, self.shape, self.bin_size, (self.delta0, self.delta1))
