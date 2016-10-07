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

class TestZone(unittest.TestCase):

    def setUp(self):
        self.filename = sample_data_file('10x10x10')

    def tearDown(self):
        os.remove(self.filename)

    # noinspection PyStatementEffect
    def test_name(self):
        tp.new_layout()
        ds = tp.data.load_tecplot(self.filename)
        zone = ds.zone('Rectangular zone')
        self.assertEqual(zone.name, 'Rectangular zone')
        zone.name = 'Ζονε'
        self.assertEqual(zone.name, 'Ζονε')
        zone = ds.zone('Ζονε')
        self.assertEqual(zone.name, 'Ζονε')
        zone.name = ''
        self.assertEqual(zone.name, '')

        # trick this zone to point to a non-existent dataset
        zone.dataset.uid += 1

        with self.assertRaises(TecplotLogicError):
            zone.name

        with self.assertRaises(TecplotLogicError):
            zone.name = 'Test'

        with self.assertRaises(TecplotLogicError):
            zone.name = None


if __name__ == '__main__':
    from .. import main
    main()
