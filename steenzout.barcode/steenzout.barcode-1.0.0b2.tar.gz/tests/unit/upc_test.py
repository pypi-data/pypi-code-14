# -*- coding: utf-8 -*-
"""Test cases for the steenzout.barcode.upc module."""

import pytest
import unittest

from steenzout.barcode import writer
from steenzout.barcode.errors import IllegalCharacterError
from steenzout.barcode.upc import UPCA


class UPCATestCase(unittest.TestCase):
    """Test case for the :py:class:`UPCA` class."""

    @staticmethod
    def assert_exception_on_validate(invalid_tt, exc):
        """"""
        for case in invalid_tt:
            with pytest.raises(exc):
                UPCA.validate(case)

    def test_build(self):
        """Test :py:func:`UPCA.build()`."""
        ref = (
            u'101010111101111010001011011'
            u'110101101110010011010101110'
            u'010111001011100101000010111'
            u'01001000010101'
        )
        instance = UPCA('639382000393')

        bar_code = instance.build()

        self.assertEqual(ref, bar_code[0])

    def test_calculate_checksum(self):
        """Test :py:func:`UPCA.calculate_checksum()`."""
        self.assertEqual(3, UPCA.calculate_checksum('63938200039'))
        self.assertEqual(3, UPCA.calculate_checksum('639382000393'))

    def test_init(self):
        """Test :py:func:`UPCA.__init__()`."""
        bar_code = UPCA('639382000393', None)

        self.assertEqual('639382000393', bar_code.code)
        self.assertTrue(isinstance(bar_code.writer, writer.SVG))

    def test_validate(self):
        """Test :py:func:`UPCA.validate()`."""
        self.assertIsNone(UPCA.validate('639382000393'))

        invalid_tt = ('63938200039', '639382000390', '6393820003930')
        UPCATestCase.assert_exception_on_validate(invalid_tt, ValueError)

        invalid_tt = ('63938200039A', '63938200039@')
        UPCATestCase.assert_exception_on_validate(invalid_tt, IllegalCharacterError)
