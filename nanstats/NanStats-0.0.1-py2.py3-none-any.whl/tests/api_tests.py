import unittest

from mock import patch
from random import randint
from nanigans.object import Credentials
from nanigans.utils import set_default_config
from nanigans.api import facebook, multichannel, publishers, events
from nanigans.models import Response

class BaseTestCase(unittest.TestCase):
    @classmethod
    def setUp(cls):
        cls.response_dict = [{}]
        cls.comma_spend = [{'fbSpend':'100,000,000'}]
    
class TestGetTimeRanges(BaseTestCase):
    @patch('nanigans.models.Adapter.get')
    def test_get_timeranges_with_dummy_vars(self, mock_send):
        mock_send.return_value = Response(data=self.response_dict)
        fb = facebook.get_timeranges()
        mc = multichannel.get_timeranges()
        pub = publishers.get_timeranges()
        self.assertIsInstance(fb, Response)
        self.assertIsInstance(mc, Response)
        self.assertIsInstance(pub, Response)

class TestGetAttributes(BaseTestCase):
    @patch('nanigans.models.Adapter.get')
    def test_get_attribtues_with_dummy_vars(self, mock_send):
        mock_send.return_value = Response(data=self.response_dict)
        fb = facebook.get_attributes()
        mc = multichannel.get_attributes()
        pub = publishers.get_attributes()
        self.assertIsInstance(fb, Response)
        self.assertIsInstance(mc, Response)
        self.assertIsInstance(pub, Response)

class TestGetMetrics(BaseTestCase):
    @patch('nanigans.models.Adapter.get')
    def test_get_metrics_with_dummy_vars(self, mock_send):
        mock_send.return_value = Response(data=self.response_dict)
        fb = facebook.get_metrics()
        mc = multichannel.get_metrics()
        pub = publishers.get_metrics()
        self.assertIsInstance(fb, Response)
        self.assertIsInstance(mc, Response)
        self.assertIsInstance(pub, Response)

class TestGetViews(BaseTestCase):
    @patch('nanigans.models.Adapter.get')
    def test_get_view_with_dummy_vars(self, mock_send):
        view = randint(10000, 99999)
        mock_send.return_value = Response(data=self.response_dict)
        fb = facebook.get_view(view)
        mc = multichannel.get_view(view)
        pub = publishers.get_view(view)
        self.assertIsInstance(fb, Response)
        self.assertIsInstance(mc, Response)
        self.assertIsInstance(pub, Response)
    
    @patch('nanigans.models.Adapter.get')
    def test_spend_parsing(self, mock_send):
        view = randint(10000, 99999)
        mock_send.return_value = Response(data=self.comma_spend)
        fb = facebook.get_view(view)
        mc = multichannel.get_view(view)
        pub = publishers.get_view(view)
        self.assertFalse(',' in fb.data[0]['fbSpend'])
        self.assertFalse(',' in mc.data[0]['fbSpend'])
        self.assertFalse(',' in pub.data[0]['fbSpend'])

class TestGetStats(BaseTestCase):
    @patch('nanigans.models.Adapter.get')
    def test_get_stats_with_dummy_vars(self, mock_send):
        mock_send.return_value = Response(data=self.response_dict)
        fb = facebook.get_stats()
        mc = multichannel.get_stats()
        pub = publishers.get_stats()
        self.assertIsInstance(fb, Response)
        self.assertIsInstance(mc, Response)
        self.assertIsInstance(pub, Response)
    
    @patch('nanigans.models.Adapter.get')
    def test_spend_parsing(self, mock_send):
        mock_send.return_value = Response(data=self.comma_spend)
        fb = facebook.get_stats()
        mc = multichannel.get_stats()
        pub = publishers.get_stats()
        self.assertFalse(',' in fb.data[0]['fbSpend'])
        self.assertFalse(',' in mc.data[0]['fbSpend'])
        self.assertFalse(',' in pub.data[0]['fbSpend'])

class TestGetEvents(BaseTestCase):
    @patch('nanigans.models.Adapter.get')
    def test_get_stats_with_dummy_vars(self, mock_send):
        mock_send.return_value = Response(data=self.comma_spend)
        toclick = events.get_time_of_click()
        toconv = events.get_time_of_conversion()
        self.assertIsInstance(toclick, Response)
        self.assertIsInstance(toconv, Response)


if __name__ == "__main__":
    test_user = 'username@fakers.com'
    test_password = 'fakePass5000'
    test_site = 123456
    auth = Credentials()
    set_default_config(test_user, test_password, test_site)

    test_cases = [
        TestGetTimeRanges,
        TestGetAttributes,
        TestGetMetrics,
        TestGetViews,
        TestGetStats,
        TestGetEvents
    ]

    for test_case in test_cases:
        suite = unittest.TestLoader().loadTestsFromTestCase(test_case)
        unittest.TextTestRunner(verbosity=5).run(suite)
