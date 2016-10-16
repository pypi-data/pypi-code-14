#!/usr/bin/env python
# encoding: utf-8

import os
import sys
import unittest


sys.path.insert(0, "..")
from py010parser import parse_file, parse_string, c_ast


class TestDefines(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass
    
    def test_pfp_define(self):
        res = parse_string("""
            #ifdef PFP
            int has_pfp;
            #else
            int no_pfp;
            #endif
        """)
        import pdb; pdb.set_trace()


if __name__ == "__main__":
        unittest.main()
