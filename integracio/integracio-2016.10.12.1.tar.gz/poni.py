#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ctypes


class CGeometry(ctypes.Structure):
    _fields_ = [
        ('distance', ctypes.c_double),
        ('poni1', ctypes.c_double),
        ('poni2', ctypes.c_double),
        ('pixelsize1', ctypes.c_double),
        ('pixelsize2', ctypes.c_double),
        ('rot1', ctypes.c_double),
        ('rot2', ctypes.c_double),
        ('rot3', ctypes.c_double),
        ('wavelength', ctypes.c_double),
        ('units', ctypes.c_int),
        ('internal_corners', ctypes.c_int)
    ]


class PoniException(ValueError):
    pass


class Poni:
    PONI_KEYS = 'pixelsize1', 'pixelsize2', 'distance', 'poni1', 'poni2', 'rot1', 'rot2', 'rot3', 'wavelength'

    def __init__(self, poni_text):
        self._poni_text = poni_text
        self._data = {}
        self._cgeometry = None
        self._read()
        self._parse()

    def _read(self):
        for i, line in enumerate(self._poni_text.splitlines()):
            if line.startswith('#') or ':' not in line:
                continue
            words = line.split(':', 1)
            key = words[0].strip().lower()
            try:
                value = words[1].strip()
            except IndexError:
                raise PoniException('Line {} of poni file seems to be corrupted'.format(i))
            else:
                self._data[key] = value

    def _parse(self):
        for key in Poni.PONI_KEYS:
            value = self._data.get(key, 0)
            if value:
                try:
                    value = float(value)
                except ValueError:
                    raise PoniException('The poni file seems to be corrupted, '
                                        'the key "{}" -> "{}" cannot be read'.format(key, value))
                else:
                    self._data[key] = value
                    self.__dict__[key] = value
            else:
                raise PoniException('The poni file seems to be invalid, '
                                    'it does not contain key "{}"'.format(key))
        self._cgeometry = CGeometry(**self._data)
        self._cgeometry.units = 0
        self._cgeometry.internal_corners = 0

    def geometry(self):
        return bytes(memoryview(self._cgeometry))

    @property
    def units(self):
        return self._cgeometry.units

    @units.setter
    def units(self, units):
        self._cgeometry.units = units

    @property
    def internal_corners(self):
        return self._cgeometry.internal_corners

    @internal_corners.setter
    def internal_corners(self, value):
        self._cgeometry.internal_corners = value
