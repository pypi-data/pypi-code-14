import os
import time
from unittest import TestCase
from .mixins import FiftyConfigMixin, InstanceRelativeMixin


class NoDefaultConfig(FiftyConfigMixin, TestCase):
    def test(self):
        """The app should use the defaults specified in flask since there is no default config.
        """
        self.assertFalse(self.app.debug)
        self.assertFalse(self.app.testing)


class DefaultConfig(InstanceRelativeMixin, TestCase):
    instance_relative_path = 'default'

    def test_debug(self):
        """The app should still be in debug mode by default.
        """
        self.assertTrue(self.app.debug)

    def test_secret(self):
        """The secret key should exist in the default config.
        """
        self.assertEqual(self.app.config['SECRET_KEY'], 'abcdefg')

    def test_missing_value(self):
        """There should be no timezone specified in the default config.
        """
        self.assertNotIn('TZ', self.app.config)


class LocalConfig(InstanceRelativeMixin, TestCase):
    instance_relative_path = 'local_override'

    def test_override(self):
        """The local config should be able to change the values of the default settings.
        """
        self.assertFalse(self.app.debug)
        self.assertEqual(self.app.config['SECRET_KEY'], 'zyxwvut')

    def test_add_config_value(self):
        """The local config should be able to add a new config variable.
        """
        self.assertTrue(self.app.config['TESTING'])

    def test_python(self):
        """The local config should be able to execute python code.
        """
        self.assertEqual(self.app.config['TZ'], time.tzname)


class ExternalConfig(InstanceRelativeMixin, TestCase):
    instance_relative_path = 'local_override'

    def test_override(self):
        """The external config should change the default secret key.
        """
        self.assertEqual(self.app.config['SECRET_KEY'], 'zyxwvut')

    def test_add_config_value(self):
        """The external config should add a new config variable.
        """
        self.assertEqual(self.app.config['TOTALLY_RANDOM'], 1234)

    def get_app_config_kwargs(self):
        return dict(config_file_name='random_config.py')


class EnvConfig(InstanceRelativeMixin, TestCase):
    instance_relative_path = 'local_override'

    def setUp(self):
        """Add an environment variable.
        """
        os.environ['FIFTY_ENV_STR'] = 'hello'
        os.environ['FIFTY_ENV_BOOL'] = 'True'
        super(EnvConfig, self).setUp()

    def test_env_var(self):
        """The app should be able to load config data from the environment.
        """
        self.assertEqual(self.app.config['ENV_STR'], 'hello')
        self.assertTrue(self.app.config['ENV_BOOL'])
