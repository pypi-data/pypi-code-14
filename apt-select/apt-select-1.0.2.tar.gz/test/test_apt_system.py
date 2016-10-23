from unittest import TestCase
# from unittest.mock import MagicMock
import apt_system

class TestGetMethods(TestCase):
    def test_get_release(self):
        """Test output of get_release"""
        valid_names = set([
            'yakkety',
            'xenial',
            'wily',
            'vivid',
            'trusty',
            'precise',
            'lucid'
        ])
        self.assertIn(apt_system.get_release()[1], valid_names)


