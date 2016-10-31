import sys

if sys.version_info < (3,1):
    import mock
    import unittest
    sys.modules['unittest.mock'] = mock
    unittest.mock = mock

    def assertIsNone(self, obj):
        return self.assertTrue(obj is None)
    unittest.TestCase.assertIsNone = assertIsNone

    if sys.version_info < (3,3):
        def assertRegex(self, text, regexp, msg=None):
            return self.assertRegexpMatches(text, regexp, msg)
        unittest.TestCase.assertRegex = assertRegex

import re
import time
import unittest

from ctypes import *
from contextlib import contextmanager
from unittest import mock

import tecplot as tp

def patch_tecutil(fn_name, **kwargs):
    return mock.patch.object(tp.tecutil._tecutil, fn_name, mock.Mock(**kwargs))

@contextmanager
def patched_tecutil(fn_name, **kwargs):
    with patch_tecutil(fn_name, **kwargs) as p:
        yield p

if False:
    # This will print out timing information for each TestCase
    @classmethod
    def setUpClass(cls):
        cls.startTime = time.time()
    @classmethod
    def tearDownClass(cls):
        print("\n{}.{}: {:.3f}".format(cls.__module__, cls.__name__, time.time() - cls.startTime))
    unittest.TestCase.setUpClass = setUpClass
    unittest.TestCase.tearDownClass = tearDownClass

from .annotation import *
from .data import *
from .export import *
from .extension import *
from .layout import *
from .legend import *
from .plot import *
from .session import *
from .tecutil import *
from .test_doc_examples import *
from .test_macro import *
from .test_version import *

def main():
    import argparse
    import logging
    import os
    import random
    import sys
    import unittest

    from argparse import ArgumentParser, SUPPRESS

    parser = ArgumentParser(usage=SUPPRESS)
    parser.add_argument('-r', '--random',
        action='store_true',
        default=False,
        help='''randomize ordering of test cases and further randomize
                test methods within each test case''')
    parser.add_argument('-d', '--debug',
        action='store_true',
        default=False,
        help='''Set logging output to DEBUG''')

    def print_help():
        parser._print_help()
        unittest.main()
    parser._print_help = parser.print_help
    parser.print_help = print_help

    args,unknown_args = parser.parse_known_args(sys.argv)

    if args.debug:
        logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    tp.session._tecinterprocess.start()

    try:
        if args.random:
            unittest.defaultTestLoader.sortTestMethodsUsing = \
                lambda *a: random.choice((-1,1))
            def suite_init(self,tests=()):
                self._tests = []
                self._removed_tests = 0
                if isinstance(tests, list):
                    random.shuffle(tests)
                self.addTests(tests)
            unittest.defaultTestLoader.suiteClass.__init__ = suite_init

        unittest.main(argv=unknown_args)

    finally:
        tp.session.stop()
