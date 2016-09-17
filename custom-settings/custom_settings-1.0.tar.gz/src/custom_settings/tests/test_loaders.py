# -*- coding: utf-8 -*-
import unittest

from .compat import mock


class LoadTest(unittest.TestCase):
    def _get_target(self):
        from ..loaders import load as func
        return func

    def test_import(self):
        """Load module test

        See: src/custom_settings/tests/settings.py
        """
        func = self._get_target()
        custom = func('custom_settings.tests.settings')
        value = custom.get('TEST_ONE')
        self.assertEqual(value, '1')

    def test_import_error(self):
        from ..exc import NoCustomSettingModuleError
        func = self._get_target()

        with self.assertRaises(NoCustomSettingModuleError):
            func('custom_settings.tests.settings_cannot_import')

    def test_object(self):
        data = mock.Mock()
        data.TEST_ONE = '1'
        func = self._get_target()
        custom = func(data)
        self.assertEqual(custom.get('TEST_ONE'), '1')
