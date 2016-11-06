# -*- coding: utf-8 -*-
import unittest
import sys
from pypiwik.decorators import track_page_view, ON_SUCCESS, ON_ERROR, ALWAYS
from pypiwik.tracker import PiwikTracker


class DecoratorTest(unittest.TestCase):

    def test_args(self):
        self.assertRaises(ValueError, track_page_view)

        self.assertRaises(ValueError, track_page_view, piwik_url='test')

        self.assertRaises(ValueError, track_page_view, site_id=1)

    @unittest.skipIf(sys.version_info < (3,0), "Mock not available in python 2.x")
    def test_when_success(self):
        from unittest.mock import MagicMock
        tracker = PiwikTracker('http://localhost', 1)
        tracker.track_page_view = MagicMock()

        @track_page_view(tracker=tracker, when=ON_SUCCESS)
        def my_func():
            pass
        my_func()

        tracker.track_page_view.assert_called()

        tracker.track_page_view.reset_mock()

        @track_page_view(tracker=tracker, when=ON_SUCCESS)
        def my_func2():
            raise Exception("lalala")

        self.assertRaises(Exception, my_func2)
        assert not tracker.track_page_view.called, "track_page_view() should not be called due to an raised exception"

    @unittest.skipIf(sys.version_info < (3,0), "Mock not available in python 2.x")
    def test_when_success(self):
        from unittest.mock import MagicMock
        tracker = PiwikTracker('http://localhost', 1)
        tracker.track_page_view = MagicMock()

        @track_page_view(tracker=tracker, when=ON_ERROR)
        def my_func():
            raise Exception("lalala")

        self.assertRaises(Exception, my_func)
        tracker.track_page_view.assert_called()

        tracker.track_page_view.reset_mock()

        @track_page_view(tracker=tracker, when=ON_ERROR)
        def my_func2():
            pass

        assert not tracker.track_page_view.called, "track_page_view() should not be called because no exception was raised"

    @unittest.skipIf(sys.version_info < (3,0), "Mock not available in python 2.x")
    def test_when_success(self):
        from unittest.mock import MagicMock
        tracker = PiwikTracker('http://localhost', 1)
        tracker.track_page_view = MagicMock()

        @track_page_view(tracker=tracker, when=ALWAYS)
        def my_func():
            pass
        my_func()

        tracker.track_page_view.assert_called()

        tracker.track_page_view.reset_mock()

        @track_page_view(tracker=tracker, when=ALWAYS)
        def my_func2():
            raise Exception("lalala")

        self.assertRaises(Exception, my_func2)
        tracker.track_page_view.assert_called()