from __future__ import unicode_literals
from __future__ import print_function

import re
import unittest

from mock import patch

from tcell_agent.appsensor.meta import AppSensorMeta
from tcell_agent.appsensor.params import GET_PARAM
from tcell_agent.config import CONFIGURATION
from tcell_agent.policies.appsensor.payloads_policy import PayloadsPolicy


class PayloadsPolicyTest(unittest.TestCase):

    def false_send_payloads_apply_test(self):
        policy_json = { "payloads": {"send_payloads": False} }
        policy = PayloadsPolicy()
        policy.from_json(policy_json)
        meta = AppSensorMeta(
            "remote_addr",
            "request_method",
            "abosolute_uri",
            "23947",
            session_id="session_id",
            user_id="user_id"
        )

        old_allow = CONFIGURATION.allow_unencrypted_appsensor_payloads
        CONFIGURATION.allow_unencrypted_appsensor_payloads = False

        with patch.object(PayloadsPolicy, 'log', return_value=None) as patched_log:
            payload = policy.apply("xss", meta, GET_PARAM, "password", "123password123", {"l": "query"}, "pattern")

            CONFIGURATION.allow_unencrypted_appsensor_payloads = old_allow

            self.assertIsNone(payload)
            patched_log.assert_called_once_with(
                'xss',
                meta,
                GET_PARAM,
                'password',
                '123password123',
                {'l': 'query'},
                'pattern')

    def true_send_payloads_false_allow_unencrypted_appfirewall_payloads_apply_test(self):
        policy_json = { "payloads": {"send_payloads": True} }
        policy = PayloadsPolicy()
        policy.from_json(policy_json)
        meta = AppSensorMeta(
            "remote_addr",
            "request_method",
            "abosolute_uri",
            "23947",
            session_id="session_id",
            user_id="user_id"
        )

        old_allow = CONFIGURATION.allow_unencrypted_appsensor_payloads
        CONFIGURATION.allow_unencrypted_appsensor_payloads = False

        with patch.object(PayloadsPolicy, 'log', return_value=None) as patched_log:
            payload = policy.apply("xss", meta, GET_PARAM, "password", "123password123", {"l": "query"}, "pattern")

            CONFIGURATION.allow_unencrypted_appsensor_payloads = old_allow

            self.assertIsNone(payload)
            patched_log.assert_called_once_with(
                'xss',
                meta,
                GET_PARAM,
                'password',
                '123password123',
                {'l': 'query'},
                'pattern')

    def true_send_payloads_true_allow_unencrypted_appfirewall_payloads_no_blacklist_no_whitelist_apply_test(self):
        policy_json = { "payloads": {"send_payloads": True, "send_blacklist": {}} }
        policy = PayloadsPolicy()
        policy.from_json(policy_json)
        meta = AppSensorMeta(
            "remote_addr",
            "request_method",
            "abosolute_uri",
            "23947",
            session_id="session_id",
            user_id="user_id"
        )

        old_allow = CONFIGURATION.allow_unencrypted_appsensor_payloads
        CONFIGURATION.allow_unencrypted_appsensor_payloads = True

        with patch.object(PayloadsPolicy, 'log', return_value=None) as patched_log:
            payload = policy.apply("xss", meta, GET_PARAM, "password", "123password123", {"l": "query"}, "pattern")

            CONFIGURATION.allow_unencrypted_appsensor_payloads = old_allow

            self.assertEquals(payload, '123password123')
            patched_log.assert_called_once_with(
                'xss',
                meta,
                GET_PARAM,
                'password',
                '123password123',
                {'l': 'query'},
                'pattern')

    def true_send_payloads_true_allow_unencrypted_appfirewall_payloads_no_blacklist_with_whitelist_missing_param_apply_test(self):
        policy_json = { "payloads": {"send_payloads": True, "send_blacklist": {}, "send_whitelist": {"username": ["*"]}} }
        policy = PayloadsPolicy()
        policy.from_json(policy_json)
        meta = AppSensorMeta(
            "remote_addr",
            "request_method",
            "abosolute_uri",
            "23947",
            session_id="session_id",
            user_id="user_id"
        )

        old_allow = CONFIGURATION.allow_unencrypted_appsensor_payloads
        CONFIGURATION.allow_unencrypted_appsensor_payloads = True

        with patch.object(PayloadsPolicy, 'log', return_value=None) as patched_log:
            payload = policy.apply("xss", meta, GET_PARAM, "password", "123password123", {"l": "query"}, "pattern")

            CONFIGURATION.allow_unencrypted_appsensor_payloads = old_allow

            self.assertEquals(payload, 'NOT_WHITELISTED')
            patched_log.assert_called_once_with(
                'xss',
                meta,
                GET_PARAM,
                'password',
                '123password123',
                {'l': 'query'},
                'pattern')

    def true_send_payloads_true_allow_unencrypted_appfirewall_payloads_no_blacklist_param_in_whitelist_but_incorrect_location_apply_test(self):
        policy_json = {
            "payloads": {
                "send_payloads": True,
                "send_blacklist": {},
                "send_whitelist": {
                    "username": ["*"],
                    "password": ["cookie"]
                }
            }
        }
        policy = PayloadsPolicy()
        policy.from_json(policy_json)
        meta = AppSensorMeta(
            "remote_addr",
            "request_method",
            "abosolute_uri",
            "23947",
            session_id="session_id",
            user_id="user_id"
        )

        old_allow = CONFIGURATION.allow_unencrypted_appsensor_payloads
        CONFIGURATION.allow_unencrypted_appsensor_payloads = True

        with patch.object(PayloadsPolicy, 'log', return_value=None) as patched_log:
            payload = policy.apply("xss", meta, GET_PARAM, "password", "123password123", {"l": "query"}, "pattern")

            CONFIGURATION.allow_unencrypted_appsensor_payloads = old_allow

            self.assertEquals(payload, 'NOT_WHITELISTED')
            patched_log.assert_called_once_with(
                'xss',
                meta,
                GET_PARAM,
                'password',
                '123password123',
                {'l': 'query'},
                'pattern')

    def true_send_payloads_true_allow_unencrypted_appfirewall_payloads_no_blacklist_param_in_whitelist_apply_test(self):
        policy_json = {
            "payloads": {
                "send_payloads": True,
                "send_blacklist": {},
                "send_whitelist": {
                    "username": ["*"],
                    "password": ["form"]
                }
            }
        }
        policy = PayloadsPolicy()
        policy.from_json(policy_json)
        meta = AppSensorMeta(
            "remote_addr",
            "request_method",
            "abosolute_uri",
            "23947",
            session_id="session_id",
            user_id="user_id"
        )

        old_allow = CONFIGURATION.allow_unencrypted_appsensor_payloads
        CONFIGURATION.allow_unencrypted_appsensor_payloads = True

        with patch.object(PayloadsPolicy, 'log', return_value=None) as patched_log:
            payload = policy.apply("xss", meta, GET_PARAM, "password", "123password123", {"l": "query"}, "pattern")

            CONFIGURATION.allow_unencrypted_appsensor_payloads = old_allow

            self.assertEquals(payload, '123password123')
            patched_log.assert_called_once_with(
                'xss',
                meta,
                GET_PARAM,
                'password',
                '123password123',
                {'l': 'query'},
                'pattern')

    def true_send_payloads_true_allow_unencrypted_appfirewall_payloads_no_whitelist_with_blacklist_missing_param_apply_test(self):
        policy_json = { "payloads": {"send_payloads": True, "send_blacklist": {"username": ["*"]}} }
        policy = PayloadsPolicy()
        policy.from_json(policy_json)
        meta = AppSensorMeta(
            "remote_addr",
            "request_method",
            "abosolute_uri",
            "23947",
            session_id="session_id",
            user_id="user_id"
        )

        old_allow = CONFIGURATION.allow_unencrypted_appsensor_payloads
        CONFIGURATION.allow_unencrypted_appsensor_payloads = True

        with patch.object(PayloadsPolicy, 'log', return_value=None) as patched_log:
            payload = policy.apply("xss", meta, GET_PARAM, "password", "123password123", {"l": "query"}, "pattern")

            CONFIGURATION.allow_unencrypted_appsensor_payloads = old_allow

            self.assertEquals(payload, '123password123')
            patched_log.assert_called_once_with(
                'xss',
                meta,
                GET_PARAM,
                'password',
                '123password123',
                {'l': 'query'},
                'pattern')

    def true_send_payloads_true_allow_unencrypted_appfirewall_payloads_no_whitelist_param_in_blacklist_but_incorrect_location_apply_test(self):
        policy_json = {
            "payloads": {
                "send_payloads": True,
                "send_blacklist": {
                    "username": ["*"],
                    "password": ["cookie"]
                }
            }
        }
        policy = PayloadsPolicy()
        policy.from_json(policy_json)
        meta = AppSensorMeta(
            "remote_addr",
            "request_method",
            "abosolute_uri",
            "23947",
            session_id="session_id",
            user_id="user_id"
        )

        old_allow = CONFIGURATION.allow_unencrypted_appsensor_payloads
        CONFIGURATION.allow_unencrypted_appsensor_payloads = True

        with patch.object(PayloadsPolicy, 'log', return_value=None) as patched_log:
            payload = policy.apply("xss", meta, GET_PARAM, "password", "123password123", {"l": "query"}, "pattern")

            CONFIGURATION.allow_unencrypted_appsensor_payloads = old_allow

            self.assertEquals(payload, '123password123')
            patched_log.assert_called_once_with(
                'xss',
                meta,
                GET_PARAM,
                'password',
                '123password123',
                {'l': 'query'},
                'pattern')

    def true_send_payloads_true_allow_unencrypted_appfirewall_payloads_no_whitelist_param_in_blacklist_apply_test(self):
        policy_json = {
            "payloads": {
                "send_payloads": True,
                "send_blacklist": {
                    "username": ["*"],
                    "password": ["form"]
                }
            }
        }
        policy = PayloadsPolicy()
        policy.from_json(policy_json)
        meta = AppSensorMeta(
            "remote_addr",
            "request_method",
            "abosolute_uri",
            "23947",
            session_id="session_id",
            user_id="user_id"
        )

        old_allow = CONFIGURATION.allow_unencrypted_appsensor_payloads
        CONFIGURATION.allow_unencrypted_appsensor_payloads = True

        with patch.object(PayloadsPolicy, 'log', return_value=None) as patched_log:
            payload = policy.apply("xss", meta, GET_PARAM, "password", "123password123", {"l": "query"}, "pattern")

            CONFIGURATION.allow_unencrypted_appsensor_payloads = old_allow

            self.assertEquals(payload, 'BLACKLISTED')
            patched_log.assert_called_once_with(
                'xss',
                meta,
                GET_PARAM,
                'password',
                '123password123',
                {'l': 'query'},
                'pattern')
