# -*- coding: utf-8 -*-
"""Test cases for the steenzout.barcode.cli package."""

import abc
import pytest
import unittest

from click.testing import CliRunner

from steenzout import barcode
from steenzout.barcode import cli


@pytest.fixture
def runner():
    return CliRunner()


class ClickTestCase(unittest.TestCase):
    """Abstract class to be used to test click commands."""
    __metaclass__ = abc.ABCMeta

    def setUp(self):
        self.runner = CliRunner()


class EncodingsTestCase(ClickTestCase):
    """Test the encodings command."""

    def test(self):
        result = self.runner.invoke(cli.cli, ('encodings',), catch_exceptions=False)
        assert not result.exception
        for enc in barcode.encodings():
            assert enc in result.output


class FormatsTestCase(ClickTestCase):
    """Test the formats command."""

    def test(self):
        result = self.runner.invoke(cli.cli, ('formats',), catch_exceptions=False)
        assert not result.exception
        for fmt in barcode.formats():
            assert fmt in result.output


class GenerateTestCase(ClickTestCase):
    """Test the generate command."""

    def test_svg(self):
        result = self.runner.invoke(
            cli.cli, (
                'generate', '-e', 'code128', '-c', '"Test Code"', 'a.svg'
            ), catch_exceptions=False)
        assert not result.exception

    def test_png(self):
        result = self.runner.invoke(
            cli.cli, (
                'generate', '-e', 'code128', '-c', '"Test Code"', 'a.png'
            ), catch_exceptions=False)
        assert not result.exception

    def test_output_to_file(self):
        result = self.runner.invoke(
            cli.cli, (
                'generate', '-e', 'code128', '-c "Test Code"', 'a.svg'
            ), catch_exceptions=False)
        assert not result.exception

    def test_output_to_stdout(self):
        result = self.runner.invoke(
            cli.cli, (
                'generate', '-e', 'code128', '-c "Test Code"', '-'
            ), catch_exceptions=False)
        assert not result.exception
