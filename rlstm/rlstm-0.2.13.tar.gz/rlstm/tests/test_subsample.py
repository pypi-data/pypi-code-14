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
sys.path.append('../sample')
from sample_timeseries import LocalTimeSeriesSampler


class TestSubsample(unittest.TestCase):
    def test_subsample(self):
        y = np.array([[[0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,\
                      1,0,1,0,0,1,0,0,0,0,0,0,1,0,0,0,0,1]]])
        X = np.array([[range(len(y[0][0]))]])
        y = np.swapaxes(y, 1, 2)
        X = np.swapaxes(X, 1, 2)
        sampler = LocalTimeSeriesSampler()
        sub_X, sub_y = sampler.subsample(X, y, pre_range=2,
                                               post_range=1,
                                               pos_frac=1)

        self.assertEqual(sub_y.shape[1], 22)
        self.assertEqual(sub_X.shape[1], 22)

        sub_X, sub_y = sampler.subsample(X, y, pre_range=3,
                                               post_range=1,
                                               pos_frac=1)

        self.assertEqual(sub_y.shape[1], 26)
        self.assertEqual(sub_X.shape[1], 26)
