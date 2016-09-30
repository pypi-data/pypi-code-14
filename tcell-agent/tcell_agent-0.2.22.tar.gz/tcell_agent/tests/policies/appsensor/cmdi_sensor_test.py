from __future__ import unicode_literals
from __future__ import print_function

import unittest

from mock import Mock, patch
from tcell_agent.appsensor.meta import AppSensorMeta
from tcell_agent.policies.appsensor import CmdiSensor

class CmdiSensorTest(unittest.TestCase):

    def create_default_sensor_test(self):
        sensor = CmdiSensor()
        self.assertEqual(sensor.enabled, False)
        self.assertEqual(sensor.exclude_headers, False)
        self.assertEqual(sensor.exclude_forms, False)
        self.assertEqual(sensor.exclude_cookies, False)
        self.assertEqual(sensor.dp, "cmdi")
        self.assertEqual(sensor.active_pattern_ids, {})
        self.assertEqual(sensor.exclusions, {})

    def with_disabled_sensor_check_test(self):
        sensor = CmdiSensor({"enabled": False})

        payloads_policy = Mock()
        with patch('tcell_agent.policies.appsensor.injection_sensor.sendEvent') as patched_send_event:
            sensor.check("get", {}, None, None, payloads_policy)
            self.assertFalse(patched_send_event.called)
            self.assertFalse(payloads_policy.apply.called)

    def with_enabled_sensor_and_no_vuln_params_check_test(self):
        sensor = CmdiSensor({"enabled": True})
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
        sensor = CmdiSensor({"enabled": True, "patterns": ["2"]})
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
            is_cmdi = sensor.check("get", meta, "dirty", "bob.txt;id", payloads_policy)
            self.assertTrue(is_cmdi)
            patched_send_event.assert_called_once_with(meta, "cmdi",  'dirty', {"l": "query"}, None, "2")
            payloads_policy.apply.assert_called_once_with("cmdi", meta, "get", "dirty", "bob.txt;id", {"l": "query"}, "2")
