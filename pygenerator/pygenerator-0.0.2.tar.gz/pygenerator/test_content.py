

TEST_BASIC = """# -*- coding: utf-8 -*-

\"\"\" basic test cases \"\"\"

import sys
import unittest


PYTHON3 = sys.version_info > (3, )


class BasicTestCase(unittest.TestCase):
    \"\"\" basic cases \"\"\"

    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        pass

    def test_basic(self):
        self.assertTrue(True)

"""
