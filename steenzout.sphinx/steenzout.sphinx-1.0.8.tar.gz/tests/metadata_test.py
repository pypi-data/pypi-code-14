# -*- coding: utf-8 -*-
"""Tests for the steenzout.sphinx.metadata module."""

import unittest


class MetadataTestCase(unittest.TestCase):
    """Test case for the version module."""

    def test_attributes(self):
        """Test the metadata module available attributes."""
        from steenzout.sphinx import metadata

        assert metadata.__version__
