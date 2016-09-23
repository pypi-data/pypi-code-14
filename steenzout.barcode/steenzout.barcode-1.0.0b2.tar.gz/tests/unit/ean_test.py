# -*- coding: utf-8 -*-
"""Test cases for the steenzout.barcode.ean module."""

import pytest
import unittest

from steenzout.barcode import writer
from steenzout.barcode.errors import IllegalCharacterError
from steenzout.barcode.ean import EAN13, EAN8


class EAN13TestCase(unittest.TestCase):
    """Test case for the :py:class:`EAN13` class."""

    @staticmethod
    def assert_exception_on_validate(invalid_tt, exc):
        """"""
        for case in invalid_tt:
            with pytest.raises(exc):
                EAN13.validate(case)

    def test_build(self):
        """Test :py:func:`EAN13.build()`."""
        ref = (
            '101000101101001110110011001001101111010011101010'
            '10110011011011001000010101110010011101000100101'
        )
        instance = EAN13('5901234123457')

        bar_code = instance.build()

        self.assertEqual(ref, bar_code[0])

    def test_calculate_checksum(self):
        """Test :py:func:`EAN13.calculate_checksum()`."""
        self.assertEqual(7, EAN13.calculate_checksum('590123412345'))
        self.assertEqual(7, EAN13.calculate_checksum('5901234123457'))

    def test_init(self):
        """Test :py:func:`EAN13.__init__()`."""
        bar_code = EAN13('5901234123457', None)

        self.assertEqual('5901234123457', bar_code.code)
        self.assertTrue(isinstance(bar_code.writer, writer.SVG))

    def test_validate(self):
        """Test :py:func:`EAN13.validate()`."""
        self.assertIsNone(EAN13.validate('5901234123457'))

        invalid_tt = ('590123412345', '5901234123453', '59012341234570')
        EAN13TestCase.assert_exception_on_validate(invalid_tt, ValueError)

        invalid_tt = ('59012341234A7', '59012341234&7')
        EAN13TestCase.assert_exception_on_validate(invalid_tt, IllegalCharacterError)


class EAN8TestCase(unittest.TestCase):
    """Test case for the :py:class:`EAN8` class."""

    @staticmethod
    def assert_exception_on_validate(invalid_tt, exc):
        """"""
        for case in invalid_tt:
            with pytest.raises(exc):
                EAN8.validate(case)

    def test_build(self):
        """Test :py:func:`EAN8.build()`."""
        ref = (
            '1010100011000110100100110101111010101000100'
            '100010011100101001000101'
        )
        instance = EAN8('40267708')

        bar_code = instance.build()

        self.assertEqual(ref, bar_code[0])

    def test_calculate_checksum(self):
        """Test :py:func:`EAN8.calculate_checksum()`."""
        self.assertEqual(8, EAN8.calculate_checksum('4026770'))
        self.assertEqual(8, EAN8.calculate_checksum('40267708'))

    def test_init(self):
        """Test :py:func:`EAN8.__init__()`."""
        bar_code = EAN8('40267708', None)

        self.assertEqual('40267708', bar_code.code)
        self.assertTrue(isinstance(bar_code.writer, writer.SVG))

    def test_validate(self):
        """Test :py:func:`EAN8.validate()`."""
        self.assertIsNone(EAN8.validate('40267708'))

        invalid_tt = ('4026770', '40267700', '402677080')
        EAN8TestCase.assert_exception_on_validate(invalid_tt, ValueError)

        invalid_tt = ('402677A8', '402677@8')
        EAN8TestCase.assert_exception_on_validate(invalid_tt, IllegalCharacterError)
