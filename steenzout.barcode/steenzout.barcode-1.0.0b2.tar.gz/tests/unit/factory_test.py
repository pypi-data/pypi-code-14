# -*- coding: utf-8 -*-
"""Test cases for the steenzout.barcode.factory module."""

import pytest
import unittest

from steenzout.barcode import errors, factory, writer


class ModuleTestCase(unittest.TestCase):
    """Test case for module functions."""

    def test_create_instance(self):
        """Test create_instance() function."""

        out = factory.create_instance('code128', 'test', None)

        assert out is not None
        assert 'test' == out.code
        assert isinstance(out.writer, writer.SVG)

    def test_create_instance_exceptions(self):
        """Test exceptions in create_instance() function."""

        tt = (None, 123, 'invalid')

        for tc in tt:
            with pytest.raises(errors.BarcodeNotFoundError):
                factory.create_instance(tc, None, None)
