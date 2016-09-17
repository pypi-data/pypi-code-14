# -*- coding: utf-8 -*-
import unittest

from .compat import mock


class CustomSettingsTest(unittest.TestCase):
    def _get_target(self, obj, *args, **kwds):
        from ..adapters import CustomSettings as target
        return target(obj, *args, **kwds)

    def _create_data(self, **kwds):
        data = mock.Mock()
        for key, value in kwds.items():
            setattr(data, key, value)
        return data

    def test_it(self):
        data = self._create_data(TEST_ONE='1')
        custom = self._get_target(data)

        value = custom.get('TEST_ONE')

        self.assertEqual(value, '1')

    def test_uer_environ(self):
        import os

        os.environ['TEST_ONE'] = '1'
        custom = self._get_target(None)

        value = custom.get('TEST_ONE', use_environ=True)
        del os.environ['TEST_ONE']

        self.assertEqual(value, '1')

    def test_uer_environ_type(self):
        import os

        os.environ['TEST_ONE'] = '1'
        custom = self._get_target(None)

        value = custom.get('TEST_ONE', use_environ=True, type_=int)
        del os.environ['TEST_ONE']

        self.assertEqual(value, 1)

    def test_type(self):
        data = self._create_data(TEST_ONE='1')
        custom = self._get_target(data)

        value = custom.get('TEST_ONE', type_=int)

        self.assertEqual(value, 1)

    def test_type_error(self):
        from ..exc import CustomSettingTypeError
        data = self._create_data(TEST_ONE='A')
        custom = self._get_target(data)

        with self.assertRaises(CustomSettingTypeError):
            custom.get('TEST_ONE', type_=int)

    def test_raise_exception(self):
        from ..exc import NoCustomSettingError
        custom = self._get_target(None)

        with self.assertRaises(NoCustomSettingError):
            custom.get('TEST_ONE', raise_exception=True)

    def test_default(self):
        custom = self._get_target(None)

        value = custom.get('TEST_ONE', default=1)

        self.assertEqual(value, 1)
