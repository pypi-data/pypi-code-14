#!/usr/bin/env python
# coding=utf-8

import unittest
from blacklist import Blacklist

class BlacklistTestCase(unittest.TestCase):
    """
    test for Hachi blacklist
    """

    def test_predict(self):
        bl = Blacklist()
        msg = u'小熊猫不吃apple又怎么了'
        self.assertEqual(bl.predict(msg), True)

if __name__ == "__main__":
    unittest.main()
