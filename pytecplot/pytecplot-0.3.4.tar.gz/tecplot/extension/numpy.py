"""
Data Access with Numpy
----------------------
"""
from __future__ import absolute_import

import numpy as np

from ctypes import memmove, POINTER, sizeof, c_double, c_float

def as_numpy_array(arr):
    dtypes = {c_double: np.float64, c_float: np.float32}
    ctype = arr.c_type
    size = arr.size
    data = np.empty((size,), dtype=dtypes[ctype])
    data_ptr = data.ctypes.data_as(POINTER(ctype))
    data_size = sizeof(ctype)*size
    memmove(data_ptr, arr.copy(), data_size)
    return data
