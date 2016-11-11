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

import numpy as np

from .vector import Vector
from .orientation import Orientation


class Transform(np.ndarray):
    def __new__(cls, *args, **kwargs):
        return np.ndarray.__new__(cls, (3, 3), dtype=np.float)

    def __init__(self, *args):
        self[:, :] = np.identity(3)
        if len(args) == 2:
            if isinstance(args[1], Iterable):
                # Argument at index 1 must be a vector
                self[:2, :2] = Orientation(args[0])
                self[:2, 2] = args[1]
            else:
                raise NotImplementedError(
                    'Argument two must be iterable and form a translation')
        elif len(args) == 1:
            if type(args[0]) == Transform:
                self[:, :] = args[0][:, :]
            else:
                return NotImplementedError(
                    'Single argument must be a Transform object')
        else:
            raise NotImplementedError('Need one or two arguments.')

    def __array_finalize__(self, obj):
        if obj is None:
            return

    def __array_wrap__(self, out_arr, context=None):
        return np.ndarray.__array_wrap__(self, out_arr, context)

    def __mul__(self, other):
        if type(other) == Vector:
            return Vector(self[:2, :2].dot(other) + self[:2, 2])
        elif type(other) == Transform:
            return self.dot(other)
        else:
            return NotImplemented

    def get_orient(self):
        """Return a reference to the orientation part of the transform. Beware that this is a reference."""
        return Orientation(self[:2, :2], byref=True)

    orient = property(get_orient)
    
    @property
    def trans(self):
        return Vector(self[:2, 2])

    @property
    def inverse(self):
        return np.linalg.inv(self)

    def invert(self):
        self[:, :] = np.linalg.inv(self)
