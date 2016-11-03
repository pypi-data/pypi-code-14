# -*- coding: utf-8 -*-
"""Test cases for the steenzout.barcode package."""

import mock
import unittest

from steenzout import barcode
from steenzout.barcode import metadata


class ModuleTestCase(unittest.TestCase):
    """Test case for the barcode package functions."""

    def test_formats(self):
        """Test formats() function"""
        expected = ('BMP', 'EPS', 'GIF', 'JPEG', 'MSP', 'PCX', 'PNG', 'SVG', 'TIFF', 'XBM')
        out = barcode.formats()

        assert isinstance(out, tuple)
        assert expected == out

    def test_formats_pil_disabled(self):
        """Test formats() function"""
        tmp = barcode.PIL_ENABLED

        barcode.PIL_ENABLED = False

        expected = ('EPS', 'SVG')
        out = barcode.formats()

        assert isinstance(out, tuple)
        assert expected == out

        barcode.PIL_ENABLED = tmp

    def test_version(self):
        """Test version() function."""
        assert metadata.__version__ == barcode.version()
