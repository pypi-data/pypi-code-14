#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ctypes
import six
from .tools import bytesbuffer


class Parfile(ctypes.Structure):
    _fields_ = [
        ('distance', ctypes.c_double),
        ('wavelength', ctypes.c_double),
        ('alpha', ctypes.c_double),
        ('beta', ctypes.c_double),
        ('xc', ctypes.c_double),
        ('yc', ctypes.c_double),
        ('ub', ctypes.c_double * (3 * 3)),
        ('d1', ctypes.c_double),  # phyx
        ('d2', ctypes.c_double),  # phyy
        ('d3', ctypes.c_double),  # phyz
        ('cell_a', ctypes.c_double),
        ('cell_b', ctypes.c_double),
        ('cell_c', ctypes.c_double),
        ('cell_alpha', ctypes.c_double),
        ('cell_beta', ctypes.c_double),
        ('cell_gamma', ctypes.c_double),
        ('b2', ctypes.c_double),  # x2 in crysalis
        ('omega0', ctypes.c_double),
        ('theta0', ctypes.c_double),
        ('kappa0', ctypes.c_double),
        ('phi0', ctypes.c_double),
        ('pixel', ctypes.c_double),
        ('inhor', ctypes.c_int),
        ('inver', ctypes.c_int),
        ('x', ctypes.c_int),
        ('y', ctypes.c_int),
        ('z', ctypes.c_int),
        ('lorentz', ctypes.c_int),
        ('dQ', ctypes.c_double),
        ('downsample', ctypes.c_int),
    ]


# noinspection PyUnusedLocal
class ParParser(object):
    def __init__(self, fname):
        self.__parfile = Parfile()
        self.x = self.y = self.z = 256
        self.lorentz = 0
        self.dQ = 0.6
        self.downsample = 1
        if six.PY3:
            parfile = open(fname, 'r', errors='ignore')
        else:
            parfile = open(fname, 'r')
        dparser = {
            'CRYSTALLOGRAPHY WAVELENGTH': self.__wavelength,
            'CRYSTALLOGRAPHY UB': self.__ub,
            'ROTSIMULATOR ALPHAANGLEINDEG': self.__alpha,
            'CCD PARAMETERS': self.__sizes,
            'ROTSIMULATOR BETAANGLEINDEG': self.__beta,
            'ROTATION DETECTORORIENTATION': self.__detorient,
            'CELL INFORMATION': self.__cell,         # for py3
            '\xa7CELL INFORMATION': self.__cell,     # for py2
            'ROTATION BEAM': self.__beam_b2,
            '            ZOOM': self.__pixelsize,
            '\xa7            ZOOM': self.__pixelsize,
            'ROTATION ZEROCORRECTION': self.__zeros,
        }
        self.ipar = parfile.readlines()
        for n, line in enumerate(self.ipar):
            for key, func in dparser.items():
                if line.startswith(key):
                    func(line, n)
                    dparser.pop(key)
                    break

    def __strip(self, s):
        return s if six.PY3 else s[1:]

    def __sizes(self, s, n):
        self.__parfile.inver, self.__parfile.inhor = map(int, s.split()[6:8])

    @property
    def inver(self):
        return self.__parfile.inver

    @property
    def inhor(self):
        return self.__parfile.inhor

    def __wavelength(self, s, n):
        self.__parfile.wavelength = float(s.split()[2])

    @property
    def wavelength(self):
        return self.__parfile.wavelength

    def __ub(self, s, n):
        # noinspection PyCallingNonCallable
        self.__parfile.ub = (ctypes.c_double * (3 * 3))(*[float(f) for f in s.split()[2:]])

    @property
    def ub(self):
        ptr = ctypes.cast(self.__parfile.ub, ctypes.POINTER(ctypes.c_double))
        return [ptr[i] for i in range(3 * 3)]

    def __alpha(self, s, n):
        self.__parfile.alpha = float(s.split()[-1])

    @property
    def alpha(self):
        return self.__parfile.alpha

    def __beta(self, s, n):
        self.__parfile.beta = float(s.split()[-1])

    @property
    def beta(self):
        return self.__parfile.beta

    def __detorient(self, s, n):
        (self.__parfile.d1, self.__parfile.d2, self.__parfile.d3, self.__parfile.distance,
         self.__parfile.xc, self.__parfile.yc) = map(float, s.split()[2:8])

    @property
    def phix(self):
        return self.__parfile.d1

    @property
    def phiy(self):
        return self.__parfile.d2

    @property
    def phiz(self):
        return self.__parfile.d3

    @property
    def dist(self):
        return self.__parfile.distance

    @property
    def xc(self):
        return self.__parfile.xc

    @property
    def yc(self):
        return self.__parfile.yc

    def __cell(self, s, n):
        for i, line in enumerate(self.ipar):
            if i <= n:
                continue
            line = self.__strip(line).replace('(', ' ').replace(')', ' ')
            if i == n + 1:
                (self.__parfile.cell_a, self.__parfile.cell_b,
                 self.__parfile.cell_c) = map(float, line.split()[::2])
            else:
                (self.__parfile.cell_alpha, self.__parfile.cell_beta,
                 self.__parfile.cell_gamma) = map(float, line.split()[::2])
            if i >= n + 2:
                break

    @property
    def cell_a(self):
        return self.__parfile.cell_a

    @property
    def cell_b(self):
        return self.__parfile.cell_b

    @property
    def cell_c(self):
        return self.__parfile.cell_c

    @property
    def cell_alpha(self):
        return self.__parfile.cell_alpha

    @property
    def cell_beta(self):
        return self.__parfile.cell_beta

    @property
    def cell_gamma(self):
        return self.__parfile.cell_gamma

    def __beam_b2(self, s, n):
        self.__parfile.be = float(self.__strip(s).split()[2])

    @property
    def beam_be(self):
        return self.__parfile.be

    def __zeros(self, s, n):
        (self.__parfile.omega0, self.__parfile.theta0, self.__parfile.kappa0,
         self.__parfile.phi0) = map(float, self.__strip(s).split()[2:6])

    @property
    def omega0(self):
        return self.__parfile.omega0

    @property
    def theta0(self):
        return self.__parfile.theta0

    @property
    def kappa0(self):
        return self.__parfile.kappa0

    @property
    def phi0(self):
        return self.__parfile.phi0

    def __pixelsize(self, s, n):
        self.__parfile.pixel = float(self.__strip(s).split()[-1])

    @property
    def pixel(self):
        return self.__parfile.pixel

    def parbuf(self):
        return bytesbuffer(self.__parfile)

    @property
    def dQ(self):
        return self.__parfile.dQ

    @dQ.setter
    def dQ(self, dQ):
        self.__parfile.dQ = dQ

    @property
    def x(self):
        return self.__parfile.x

    @x.setter
    def x(self, x):
        self.__parfile.x = x

    @property
    def y(self):
        return self.__parfile.y

    @y.setter
    def y(self, y):
        self.__parfile.y = y

    @property
    def z(self):
        return self.__parfile.z

    @z.setter
    def z(self, z):
        self.__parfile.z = z

    @property
    def lorentz(self):
        return self.__parfile.lorentz

    @lorentz.setter
    def lorentz(self, lorentz):
        self.__parfile.lorentz = lorentz

    @property
    def downsample(self):
        return self.__parfile.downsample

    @downsample.setter
    def downsample(self, downsample):
        self.__parfile.downsample = downsample
