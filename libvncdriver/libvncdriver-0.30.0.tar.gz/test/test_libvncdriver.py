#!/usr/bin/env python
# test_libvncdriver.py - module-level unit tests

import unittest
import libvncdriver

class TestLibvncdriverError(unittest.TestCase):
    ''' Test raising libvncdriver.Error exception '''
    def test_meraise(self):
        with self.assertRaises(libvncdriver.Error):
            libvncdriver.meraise()

if __name__ == '__main__':
    unittest.main()
