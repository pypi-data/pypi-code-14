#!/usr/bin/env python
# -*- coding: utf-8 -*-

import binascii


class Distortion:
    def __init__(self):
        self._dis = None
        self._det = None
        self._spline_checksum = 0

    def init(self, spline):
        if spline:
            checksum = binascii.crc32(spline.encode())
            res = checksum == self._spline_checksum
            self._spline_checksum = checksum
            if not res:
                from pyFAI import detectors, distortion
                self._det = detectors.FReLoN(spline)
                self._dis = distortion.Distortion(self._det)
        else:
            self._det = None
            self._dis = None
            self._spline_checksum = 0

    def __call__(self, image):
        if self._dis is not None:
            try:
                image.array = self._dis.correct(image.array)
            except AttributeError:
                image = self._dis.correct(image)
        return image
