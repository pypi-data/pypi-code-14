# -*- coding: utf-8 -*-
"""Test cases for the steenzout.barcode.base module."""

import pytest
import unittest

from steenzout.barcode import base, writer


class MockBarcode(base.Barcode):
    """Mock bar code class."""

    digits = 2

    @staticmethod
    def calculate_checksum(code):
        """(int): code checksum."""
        return int(code)

    @staticmethod
    def validate(code):
        return

    def build(self):
        return self.code

    def get_fullcode(self):
        return self.code

    def write(self, fp, options):
        return


class MockWriter(writer.Base):
    def save(self, filename, output):
        pass


class BarcodeTestCase(unittest.TestCase):
    """Test case for the :py:class:`steenzout.barcode.base.Barcode` class."""

    def setUp(self):
        self.code = MockBarcode('12', None)

    def test_property_checksum(self):
        self.assertEqual(12, self.code.checksum)

    def test_property_writer(self):
        self.assertTrue(isinstance(self.code.writer, writer.SVG))

        self.code.writer = MockWriter()
        self.assertTrue(isinstance(self.code.writer, MockWriter))

        with pytest.raises(ValueError):
            self.code.writer = 'invalid'
