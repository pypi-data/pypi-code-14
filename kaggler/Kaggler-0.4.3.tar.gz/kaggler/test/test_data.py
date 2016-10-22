import numpy as np
import os
import unittest

from kaggler.preprocessing import Normalizer, LabelEncoder, OneHotEncoder


DUMMY_X1 = np.array([[3, 'a'],
                     [3, 'b'],
                     [1, 'a'],
                     [np.nan, 'c'],
                     [np.nan, 'b'],
                     [0, 'c']])

class TestLabelEncoder(unittest.TestCase):

    def setUp(self):
        self.encoder = LabelEncoder(min_obs=2)

    def test_fit(self):
        self.encoder.fit(DUMMY_X1)
            
        # check if target values are correct
        self.assertEqual(self.encoder.label_maxes, [2, 3])


if __name__ == '__main__':
    unittest.main()

