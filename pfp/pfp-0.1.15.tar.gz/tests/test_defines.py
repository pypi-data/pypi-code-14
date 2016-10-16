#!/usr/bin/env python
# encoding: utf-8

import os
import struct
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pfp
import utils


class TestDefines(utils.PfpTestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_pfp_define(self):
        pass

    def test_pfp_version_define(self):
        dom = self._test_parse_build(
            "",
            """
                Printf("%s", PFP_VERSION);
            """,
            #stdout     = pfp.__version__,
            predefines = True
        )


if __name__ == "__main__":
    unittest.main()
