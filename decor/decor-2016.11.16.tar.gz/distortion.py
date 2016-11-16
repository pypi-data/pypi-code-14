#!/usr/bin/env python
# -*- coding: utf-8 -*-

import binascii
import threading
import numpy as np
from .spline import Spline
from . import _decor


class Distortion:
    def __init__(self):
        self._capsule = None
        self._lock = threading.Lock()
        self.pos = None
        self.delta0 = None
        self.delta1 = None
        self.spline = None
        self.spline_file = None
        self.shape = None
        self.bin_size = None
        self.lut = None
        self.bin_size_c = None
        self._spline_checksum = 0

    def init(self, spline):
        with self._lock:
            if spline:
                checksum = binascii.crc32(spline.encode())
                res = checksum == self._spline_checksum
                self._spline_checksum = checksum
                if not res:
                    self.spline_file = spline
                    self.spline = Spline(spline)
                    self._capsule = _decor.init_distortion()
            else:
                self._spline_checksum = 0
                self._capsule = None
            if self._capsule is None and self.shape is not None:
                self._capsule = _decor.init_distortion()
                self._init_lut()

    def check_shape(self, shape):
        if self.shape != shape:
            self._capsule = None
            self.shape = shape
            self.init(self.spline_file)

    def __call__(self, image):
        if self._capsule:
            try:
                self.check_shape(image.array.shape)
                image.array = self._correct(image.array)
            except AttributeError:
                self.check_shape(image.shape)
                image = self._correct(image)
        return image

    def _correct(self, image):
        buf = np.ascontiguousarray(image, np.float32).tobytes()
        return np.frombuffer(_decor.correct_lut(self._capsule, buf), np.float32).reshape(self.shape)

    def calc_cartesian_positions(self, d1, d2):
        d1c = d1 + 0.5
        d2c = d2 + 0.5
        dx = self.spline.func_x_y(d2c, d1c, 0)
        dy = self.spline.func_x_y(d2c, d1c, 1)
        return dy + d1c, dx + d2c

    def _init_lut(self):
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
        delta0 = int((np.ceil(pos_corners[1:, :, 0]) - np.floor(pos_corners[:-1, :, 0])).max())
        delta1 = int((np.ceil(pos_corners[:, 1:, 1]) - np.floor(pos_corners[:, :-1, 1])).max())
        buf = np.ascontiguousarray(self.pos.ravel(), np.float32).tobytes()
        _decor.calc_lut(self._capsule, dim1, dim2, delta0, delta1, buf)
