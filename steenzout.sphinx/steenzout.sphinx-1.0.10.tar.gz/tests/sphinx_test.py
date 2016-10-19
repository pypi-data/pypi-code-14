# -*- coding: utf-8 -*-
"""Tests for the steenzout.sphinx package."""

import filecmp
import unittest

from steenzout.sphinx import ResourceGenerator


class ResourceGeneratorTestCase(unittest.TestCase):
    """Tests for the steenzout.sphinx.ResourceGenerator class."""

    @staticmethod
    def _compare_output(filename, output):

        assert output is not None

        with open('tests/output/%s' % filename, 'w') as fd:
            fd.write('%s' % output)

        assert filecmp.cmp(
            'tests/resources/%s' % filename,
            'tests/output/%s' % filename)

    def setUp(self):
        self.generator = ResourceGenerator('steenzout', 'steenzout.sphinx')

    def test_conf(self):
        conf = self.generator.conf()

        self._compare_output('conf.py', conf)

    def test_makefile(self):
        makefile = self.generator.makefile()

        self._compare_output('Makefile', makefile)
