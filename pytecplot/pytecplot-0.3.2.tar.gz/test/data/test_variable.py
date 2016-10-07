# coding: utf-8
from __future__ import unicode_literals

import base64
import os
import platform
import sys
import unittest
import zlib

from contextlib import contextmanager
from ctypes import *
from tempfile import NamedTemporaryFile
from unittest.mock import patch, Mock

import tecplot as tp
from tecplot import session
from tecplot.exception import *

from ..sample_data import sample_data_file

class TestVariable(unittest.TestCase):

    def setUp(self):
        self.filename = sample_data_file('10x10x10')

    def tearDown(self):
        os.remove(self.filename)

    def test_name(self):
        tp.new_layout()
        ds = tp.data.load_tecplot(self.filename)
        xvar = ds.variable('X')
        self.assertEqual(xvar.name, 'X')
        xvar.name = 'Xα'
        self.assertEqual(xvar.name, 'Xα')
        xvar = ds.variable('Xα')
        self.assertEqual(xvar.name, 'Xα')
        xvar.name = ''
        self.assertEqual(xvar.name, '')

        with self.assertRaises(TecplotLogicError):
            xvar.name = None

        xvar.dataset.uid += 1 # trick this variable to point to a non-existant dataset
        with self.assertRaises(TecplotLogicError):
            xvar.name
        with self.assertRaises(TecplotLogicError):
            xvar.name = 'Test'

if __name__ == '__main__':
    from .. import main
    main()
