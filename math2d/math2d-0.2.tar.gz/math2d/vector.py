# coding=utf-8

"""
"""

__author__ = "Morten Lind"
__copyright__ = "Morten Lind 2016"
__credits__ = ["Morten Lind"]
__license__ = "GPLv3"
__maintainer__ = "Morten Lind"
__email__ = "morten@lind.dyndns.dk"
__status__ = "Development"


from numbers import Number
from collections import Iterable

import numpy as np
from . import EPS


class Vector(np.ndarray):
    def __new__(cls, *args):
        return np.ndarray.__new__(cls, (2,), dtype=np.float)

    def __init__(self, *args):
        if len(args) > 0:
            self[:] = np.array(args).flatten()[:2]
        else:
            self[:] = np.zeros(2, dtype=np.float)

    def __array_finalize__(self, obj):
        if obj is None:
            return

    def __array_wrap__(self, out_arr, context=None):
        return np.ndarray.__array_wrap__(self, out_arr, context)

    def __getattr__(self, name):
        if name == 'x':
            return self[0]
        elif name == 'y':
            return self[1]
        else:
            raise AttributeError('Attribute "{}" not found in Vector'
                                 .format(name))

    def __setattr__(self, name, val):
        if name == 'x':
            self[0] = val
        elif name == 'y':
            self[1] = val
        else:
            object.__setattr__(self, name, val)

    def __mul__(self, other):
        """Return the dot product of the two vectors."""
        if type(other) == Vector:
            return self.dot(other)
        elif isinstance(other, Number):
            return other * self[:]
        else:
            return NotImplemented

    def dist(self, other):
        if type(other) == Vector:
            return (self - other).norm
        else:
            raise NotImplementedError

    def cross(self, other):
        """Cross product with 'other'."""
        return np.float(np.cross(self, other))

    def angle(self, other):
        """Numerical angle with 'other' in [0, pi]."""
        return np.arccos(self * other / (self.norm * other.norm))

    def signed_angle_to(self, other):
        """Signed rotation angle to 'other' in [-pi; pi]."""
        cprod = self.cross(other)
        if np.abs(cprod) < EPS:
            cprod = 1.0
        return np.sign(cprod) * self.angle(other)

    @property
    def perp(self):
        """Return the right-handed perpendicular vector of this vector."""
        return Vector(np.cross([0, 0, 1], self))

    @property
    def norm(self):
        """Return the Euclidean norm of the vector."""
        return np.linalg.norm(self)

    def normalize(self):
        """In-place normalize the vector."""
        self /= self.norm
