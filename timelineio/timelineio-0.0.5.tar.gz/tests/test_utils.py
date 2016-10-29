# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
import unittest

import mock

from timelineio.utils import env_to_bool


@mock.patch('timelineio.utils.os')
class EnvToBoolTestCase(unittest.TestCase):
    def test_positive_values(self, os_patched):
        os_patched.environ.get.return_value = 'True'
        self.assertTrue(env_to_bool('WHATEVER (IT IS MOCKED)'))

        os_patched.environ.get.return_value = '1'
        self.assertTrue(env_to_bool('WHATEVER (IT IS MOCKED)'))

        os_patched.environ.get.return_value = 't'
        self.assertTrue(env_to_bool('WHATEVER (IT IS MOCKED)'))

        os_patched.environ.get.return_value = 'y'
        self.assertTrue(env_to_bool('WHATEVER (IT IS MOCKED)'))

        os_patched.environ.get.return_value = 'yes'
        self.assertTrue(env_to_bool('WHATEVER (IT IS MOCKED)'))

    def test_negative_values(self, os_patched):
        os_patched.environ.get.return_value = 'False'
        self.assertFalse(env_to_bool('WHATEVER (IT IS MOCKED)'))

        os_patched.environ.get.return_value = '0'
        self.assertFalse(env_to_bool('WHATEVER (IT IS MOCKED)'))

        os_patched.environ.get.return_value = 'f'
        self.assertFalse(env_to_bool('WHATEVER (IT IS MOCKED)'))

        os_patched.environ.get.return_value = 'n'
        self.assertFalse(env_to_bool('WHATEVER (IT IS MOCKED)'))

        os_patched.environ.get.return_value = 'no'
        self.assertFalse(env_to_bool('WHATEVER (IT IS MOCKED)'))

    def test_invalid_values(self, os_patched):
        os_patched.environ.get.return_value = 'Hamster'
        self.assertRaises(ValueError, env_to_bool, 'WHATEVER (IT IS MOCKED)')

    def test_defaults(self, os_patched):
        os_patched.environ.get.return_value = None
        self.assertFalse(env_to_bool('WHATEVER (IT IS MOCKED)'))
        self.assertFalse(env_to_bool('WHATEVER (IT IS MOCKED)', default=False))
        self.assertTrue(env_to_bool('WHATEVER (IT IS MOCKED)', default=True))
