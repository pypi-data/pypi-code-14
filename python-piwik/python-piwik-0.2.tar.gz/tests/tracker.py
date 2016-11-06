# -*- coding: utf-8 -*-
import json
import unittest
import datetime
import pytz
from pypiwik.tracker import PiwikTracker, PARAMETERS, AUTH_RESTRICTED_PARAMS


class TrackerTest(unittest.TestCase):

    def test_init(self):
        tracker = PiwikTracker('http://localhost', 1)

        for property_name in PARAMETERS.keys():
            assert hasattr(tracker, property_name), "Missing property on %s: %s" % (tracker, property_name)

    def test_from_request(self):
        class FakeRequest(object):
            META = {
                'HTTP_USER_AGENT': 'ua',
                'HTTP_REFERER': 'ref',
                'HTTP_ACCEPT_LANGUAGE': 'lang'
            }

        tracker = PiwikTracker('http://localhost', 1, FakeRequest())
        assert tracker.user_agent == 'ua'
        assert tracker.referer == 'ref'
        assert tracker.lang == 'lang'
        assert tracker.url is None
        assert tracker.client_ip is None

    def test_from_request_with_url(self):
        class FakeRequest(object):
            def build_absolute_uri(self):
                return "http://foobar.local/test123"

        tracker = PiwikTracker('http://localhost', 1, FakeRequest())
        assert tracker.url == "http://foobar.local/test123"

    def test_from_request_client_ip(self):
        class FakeRequest(object):
            META = { 'HTTP_X_FORWARDED_FOR': '127.1.2.3' }

        tracker = PiwikTracker('http://localhost', 1, FakeRequest())
        assert tracker.client_ip == '127.1.2.3'

    def test_from_bad_request(self):
        class FakeRequest(object):
            pass

        tracker = PiwikTracker('http://localhost', 1, FakeRequest())
        self.assertDictEqual({'apiv': PiwikTracker.API_VERSION, 'idsite': 1, 'rec': '1'}, tracker._build_parameters())

        class FakeRequest2(object):
            META = "test"

        tracker = PiwikTracker('http://localhost', 1, FakeRequest2())
        self.assertDictEqual({'apiv': PiwikTracker.API_VERSION, 'idsite': 1, 'rec': '1'}, tracker._build_parameters())


    def test_parameters(self):
        site_id = 123
        tracker = PiwikTracker('http://localhost', site_id)

        for property_name in PARAMETERS.keys():
            if property_name in ('page_custom_vars', 'visit_custom_vars'):
                continue
            setattr(tracker, property_name, 'test')

        params = tracker._build_parameters()
        assert 'apiv' in params and params['apiv'] == PiwikTracker.API_VERSION, "Wrong or missing API version"
        assert 'idsite' in params and params['idsite'] == site_id, 'Wrong or missing site id'
        assert 'rec' in params and params['rec'] == '1', 'Wrong or missing "rec" parameter'

        for property_name, parameter_name in PARAMETERS.items():
            if not parameter_name:
                continue
            if property_name in ('page_custom_vars', 'visit_custom_vars'):
                continue
            assert parameter_name in params, "Parameter %s not found in dict" % parameter_name
            assert params[parameter_name] == getattr(tracker, property_name)

    def test_custom_vars_conversion(self):
        tracker = PiwikTracker('http://localhost', 1)
        tracker.page_custom_vars['foo'] = 'bar'

        params = tracker._build_parameters()

        cvars = json.loads(params['cvar'])
        self.assertDictEqual(cvars, {
            '1': ['foo', 'bar']
        })

    def test_boolean_parameter_conversion(self):
        tracker = PiwikTracker('http://localhost', 1)
        tracker.track_bots = True

        params = tracker._build_parameters()
        assert params['bots'] == 1, "Boolean conversion from True to 1 failed"

    def test_datetime_parameter_conversion(self):
        tracker = PiwikTracker('http://localhost', 1)
        tracker.token_auth = 'foobar'
        tracker.client_dt = datetime.datetime(2015, 7, 12, 11, 22, 33, tzinfo=pytz.UTC)

        params = tracker._build_parameters()
        assert params['cdt'] == '2015-07-12 11:22:33', "DateTime conversion to string failed"

    def test_skip_auth_params_on_unauth_request(self):
        tracker = PiwikTracker('http://localhost', 1)

        for p in AUTH_RESTRICTED_PARAMS:
            if p == "token_auth":
                continue

            setattr(tracker, p, 'test')

        params = tracker._build_parameters()
        assert not any((k in AUTH_RESTRICTED_PARAMS for k in params.keys())),\
            "Tracking variables with authentication required should be filtered out if token_auth is not set"

    def test_request_headers_with_spoof(self):
        tracker = PiwikTracker('http://localhost', 1)

        headers = tracker.build_request_headers({})
        self.assertDictEqual(headers, {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
        })

    def test_request_headers_with_spoof_params(self):
        tracker = PiwikTracker('http://localhost', 1)

        headers = tracker.build_request_headers({'ua': 'fake user agent'})
        self.assertDictEqual(headers, {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'User-Agent': 'fake user agent'
        })

    def test_request_headers_with_spoof_headers(self):
        tracker = PiwikTracker('http://localhost', 1)
        tracker.request_headers['foo'] = 'bar'

        headers = tracker.build_request_headers({})
        self.assertDictEqual(headers, {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'foo': 'bar'
        })

    def test_request_headers_without_spoof(self):
        tracker = PiwikTracker('http://localhost', 1)
        tracker.spoof_request = False

        headers = tracker.build_request_headers({'user_agent': 'fake user agent'})
        self.assertDictEqual(headers, {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
        })

    def test_tracker_url_builder(self):
        tracker = PiwikTracker('http://localhost', 1)
        assert tracker.php_url == "http://localhost/piwik.php"

        tracker.piwik_php_file = 'test123.php'
        assert tracker.php_url == "http://localhost/test123.php"

    def test_js_url_builder(self):
        tracker = PiwikTracker('http://localhost', 1)
        assert tracker.js_url == "http://localhost/piwik.js"

        tracker.piwik_js_file = 'test123.js'
        assert tracker.js_url == "http://localhost/test123.js"
