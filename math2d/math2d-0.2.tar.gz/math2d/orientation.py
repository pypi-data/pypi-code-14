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


from collections import Iterable
from numbers import Number

import numpy as np

from .vector import Vector
import math2d


class Orientation(np.ndarray):

    def __new__(cls, *args, **kwargs):
        return np.ndarray.__new__(cls, (2, 2), dtype=np.float)

    def __init__(self, *args, **kwargs):
        if len(args) == 0:
            self[:, :] = np.zeros((2, 2))
        elif len(args) == 1:
            if isinstance(args[0], Iterable):
                self[:, :] = args[0]
            else:
                a = args[0]
                self[:, :] = [[np.cos(a), -np.sin(a)],
                              [np.sin(a), np.cos(a)]]
        else:
            raise NotImplementedError('Need none or one argument.')

    def __array_finalize__(self, obj):
        if obj is None:
            return

    def __array_wrap__(self, out_arr, context=None):
        return np.ndarray.__array_wrap__(self, out_arr, context)

    def __mul__(self, other):
        if type(other) == Vector:
            return Vector(self.dot(other))
        elif type(other) == Orientation:
            return Orientation(self.dot(other))
        else:
            return NotImplemented

    # @classmethod
    # def new_by_ref(cls, data):
    #     """Create a new Orientation object with reference to 'data'."""
    #     o = Orientation()
    #     if isinstance(data, Orientation):
    #         pass

    @property
    def angle(self):
        """Return the angle in (0;2pi) represented by this orientation."""
        return np.arctan2(*self[::-1, 0]) % (2 * np.pi)

    @property
    def inverse(self):
        return self.T

    def invert(self):
        self[:, :] = self.T
