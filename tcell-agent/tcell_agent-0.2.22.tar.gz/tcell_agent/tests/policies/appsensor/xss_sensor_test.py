from __future__ import unicode_literals
from __future__ import print_function

import re
import unittest

from mock import Mock, patch
from tcell_agent.appsensor.meta import AppSensorMeta
from tcell_agent.appsensor.rules import AppSensorRuleManager
from tcell_agent.policies.appsensor import XssSensor

class XssSensorTest(unittest.TestCase):

    def create_default_sensor_test(self):
        sensor = XssSensor()
        self.assertEqual(sensor.enabled, False)
        self.assertEqual(sensor.exclude_headers, False)
        self.assertEqual(sensor.exclude_forms, False)
        self.assertEqual(sensor.exclude_cookies, False)
        self.assertEqual(sensor.dp, "xss")
        self.assertEqual(sensor.libinjection, False)
        self.assertEqual(sensor.active_pattern_ids, {})
        self.assertEqual(sensor.exclusions, {})

    def create_enabled_sensor_test(self):
        sensor = XssSensor({"enabled": True})
        self.assertEqual(sensor.enabled, True)
        self.assertEqual(sensor.exclude_headers, False)
        self.assertEqual(sensor.exclude_forms, False)
        self.assertEqual(sensor.exclude_cookies, False)
        self.assertEqual(sensor.dp, "xss")
        self.assertEqual(sensor.libinjection, False)
        self.assertEqual(sensor.active_pattern_ids, {})
        self.assertEqual(sensor.exclusions, {})

    def create_excluded_headers_sensor_test(self):
        sensor = XssSensor({"exclude_headers": True})
        self.assertEqual(sensor.enabled, False)
        self.assertEqual(sensor.exclude_headers, True)
        self.assertEqual(sensor.exclude_forms, False)
        self.assertEqual(sensor.exclude_cookies, False)
        self.assertEqual(sensor.dp, "xss")
        self.assertEqual(sensor.libinjection, False)
        self.assertEqual(sensor.active_pattern_ids, {})
        self.assertEqual(sensor.exclusions, {})

    def create_excluded_forms_sensor_test(self):
        sensor = XssSensor({"exclude_forms": True})
        self.assertEqual(sensor.enabled, False)
        self.assertEqual(sensor.exclude_headers, False)
        self.assertEqual(sensor.exclude_forms, True)
        self.assertEqual(sensor.exclude_cookies, False)
        self.assertEqual(sensor.dp, "xss")
        self.assertEqual(sensor.libinjection, False)
        self.assertEqual(sensor.active_pattern_ids, {})
        self.assertEqual(sensor.exclusions, {})

    def create_excluded_cookies_sensor_test(self):
        sensor = XssSensor({"exclude_cookies": True})
        self.assertEqual(sensor.enabled, False)
        self.assertEqual(sensor.exclude_headers, False)
        self.assertEqual(sensor.exclude_forms, False)
        self.assertEqual(sensor.exclude_cookies, True)
        self.assertEqual(sensor.dp, "xss")
        self.assertEqual(sensor.libinjection, False)
        self.assertEqual(sensor.active_pattern_ids, {})
        self.assertEqual(sensor.exclusions, {})

    def create_libinjection_sensor_test(self):
        sensor = XssSensor({"libinjection": True})
        self.assertEqual(sensor.enabled, False)
        self.assertEqual(sensor.exclude_headers, False)
        self.assertEqual(sensor.exclude_forms, False)
        self.assertEqual(sensor.exclude_cookies, False)
        self.assertEqual(sensor.dp, "xss")
        self.assertEqual(sensor.libinjection, True)
        self.assertEqual(sensor.active_pattern_ids, {})
        self.assertEqual(sensor.exclusions, {})

    def create_active_pattern_ids_sensor_test(self):
        sensor = XssSensor({"patterns": ["1", "2", "3"]})
        self.assertEqual(sensor.enabled, False)
        self.assertEqual(sensor.exclude_headers, False)
        self.assertEqual(sensor.exclude_forms, False)
        self.assertEqual(sensor.exclude_cookies, False)
        self.assertEqual(sensor.dp, "xss")
        self.assertEqual(sensor.libinjection, False)
        self.assertEqual(sensor.active_pattern_ids, {"1": True, "2": True, "3": True})
        self.assertEqual(sensor.exclusions, {})

    def create_exclusions_sensor_test(self):
        sensor = XssSensor({"exclusions": {"word": ["form", "header"]}})
        self.assertEqual(sensor.enabled, False)
        self.assertEqual(sensor.exclude_headers, False)
        self.assertEqual(sensor.exclude_forms, False)
        self.assertEqual(sensor.exclude_cookies, False)
        self.assertEqual(sensor.dp, "xss")
        self.assertEqual(sensor.libinjection, False)
        self.assertEqual(sensor.active_pattern_ids, {})
        self.assertEqual(sensor.exclusions, {"word": ["form", "header"]})

    def with_disabled_sensor_check_test(self):
        sensor = XssSensor({"enabled": False})

        payloads_policy = Mock()
        with patch('tcell_agent.policies.appsensor.injection_sensor.sendEvent') as patched_send_event:
            sensor.check("get", {}, None, None, payloads_policy)
            self.assertFalse(patched_send_event.called)
            self.assertFalse(payloads_policy.apply.called)

    def with_enabled_sensor_and_no_vuln_params_check_test(self):
        sensor = XssSensor({"enabled": True})
        meta = AppSensorMeta(
            "remote_addr",
            "request_method",
            "abosolute_uri",
            "23947",
            session_id="session_id",
            user_id="user_id"
        )

        payloads_policy = Mock()
        with patch('tcell_agent.policies.appsensor.injection_sensor.sendEvent') as patched_send_event:
            sensor.check("get", meta, None, None, payloads_policy)
            self.assertFalse(patched_send_event.called)
            self.assertFalse(payloads_policy.apply.called)

    def with_enabled_sensor_and_vuln_params_check_test(self):
        sensor = XssSensor({"enabled": True, "patterns": ["1"]})
        meta = AppSensorMeta(
            "remote_addr",
            "request_method",
            "abosolute_uri",
            "23947",
            session_id="session_id",
            user_id="user_id"
        )

        payloads_policy = Mock()
        payloads_policy.apply.return_value = None
        with patch('tcell_agent.policies.appsensor.injection_sensor.sendEvent') as patched_send_event:
            is_xss = sensor.check("get", meta, "dirty", "<script></script>", payloads_policy)
            self.assertTrue(is_xss)
            patched_send_event.assert_called_once_with(meta, "xss",  'dirty', {"l": "query"}, None, "1")
            payloads_policy.apply.assert_called_once_with("xss", meta, "get", "dirty", "<script></script>", {"l": "query"}, "1")

    def with_enabled_sensor_and_vuln_params_and_matching_excluded_route_check_test(self):
        sensor = XssSensor({"enabled": True, "patterns": ["1"], "exclude_routes": ["23947"]})
        meta = AppSensorMeta(
            "remote_addr",
            "request_method",
            "abosolute_uri",
            "23947",
            session_id="session_id",
            user_id="user_id"
        )

        payloads_policy = Mock()
        with patch('tcell_agent.policies.appsensor.injection_sensor.sendEvent') as patched_send_event:
            is_xss = sensor.check("get", meta, "dirty", "<script></script>", payloads_policy)
            self.assertFalse(is_xss)
            self.assertFalse(patched_send_event.called)

    def with_enabled_sensor_and_vuln_params_and_nonmatching_excluded_route_check_test(self):
        sensor = XssSensor({"enabled": True, "patterns": ["1"], "exclude_routes": ["nonmatching"]})
        meta = AppSensorMeta(
            "remote_addr",
            "request_method",
            "abosolute_uri",
            "23947",
            session_id="session_id",
            user_id="user_id"
        )

        payloads_policy = Mock()
        payloads_policy.apply.return_value = None
        with patch('tcell_agent.policies.appsensor.injection_sensor.sendEvent') as patched_send_event:
            is_xss = sensor.check("get", meta, "dirty", "<script></script>", payloads_policy)
            self.assertTrue(is_xss)
            patched_send_event.assert_called_once_with(meta, "xss",  'dirty', {"l": "query"}, None, "1")

    def does_not_override_get_ruleset_test(self):
        with patch.object(AppSensorRuleManager, 'get_ruleset_for', return_value=None) as patched_get_ruleset_for:
            sensor = XssSensor()
            sensor.get_ruleset()
            patched_get_ruleset_for.assert_called_once_with('xss')
