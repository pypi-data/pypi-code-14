import ctypes
import os
import numpy as np
import sys





__all__ = ['reduction']
	
	
_path = os.path.dirname(__file__) + "/.."


libvec = np.ctypeslib.load_library('alloc', _path)
libvec.plib_fast_reduction.argtypes=[np.ctypeslib.ndpointer(ctypes.c_float, flags="C_CONTIGUOUS,ALIGNED"),ctypes.c_uint64]
libvec.plib_fast_reduction.restype=ctypes.c_float


def reduction(tab):
	"""
	Compute sum of all tab's elements
	Parameters
	----------
	tab: C_CONTINMGUOUS, ALIGNED numpy array of ctypes.c_float
	Returns
	--------
	sum of all tab's elements
	"""
	return libvec.plib_fast_reduction(tab, tab.size)
