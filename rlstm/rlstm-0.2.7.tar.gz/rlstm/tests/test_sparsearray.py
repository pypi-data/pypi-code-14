''' Run a quick example pipeline and see if the
    pipeline can be loaded and saved correctly
    with Marmalade
'''

import os
import shutil
import unittest
import tempfile
import numpy as np

import sys
sys.path.append('..')
from timeseries_util import sarray


class TestSparseArray(unittest.TestCase):
    def test_sparsearray(self):
        fenceposts = np.array([0,4,10,22,27,28,30])
        num_dim = 3
        num_mix = 30
        array_2d = np.arange(num_dim*num_mix).reshape((num_dim, num_mix))

        sarray_2d = sarray(array_2d, fenceposts)

        self.assertEqual(sarray_2d._map(3, 2), 24)
        self.assertEqual(sarray_2d._map(0, 1), 1)
        self.assertEqual(sarray_2d._map(6, 2), 32)
        self.assertEqual(sum(sarray_2d.slice(([0], [2], [3]))), 13)
        self.assertEqual(
            list(sarray_2d.slice(([0, 1, 2], [0], [1,2,3])).flatten()),
            list(np.array([1,2,3,31,32,33,61,62,63])))
        self.assertEqual(sarray_2d.apply(np.sum), 4005)

    def test_sparsearray_dummy(self):
        array_3d = np.arange(12).reshape((2,3,2))
        array_2d = np.arange(12).reshape((2,6))
        fenceposts = np.array([0, 2, 4, 6])
        sarray_2d = sarray(array_2d, fenceposts)
        self.assertEqual(sum(sarray_2d.slice(([0], [0], [0]))), array_3d[0, 0, 0])
        self.assertEqual(list(sarray_2d.slice(([0], [0], [0,1]))), list(array_3d[0, 0, [0,1]]))
        self.assertEqual(sarray_2d.slice(([0,1], [0,1], [0,1,2])), array_3d)

        self.assertEqual(sarray_2d.slice((0, 0, 0)), 0)
        self.assertEqual(list(sarray_2d.slice((0, 0, [0]))), [0])
        self.assertEqual(list(sarray_2d.slice((0, 0, [[0]]))), [[0]])
