from __future__ import unicode_literals
from __future__ import print_function

import json
import unittest

from mock import call, patch
from django.utils.datastructures import MultiValueDict
from tcell_agent.appsensor.meta import AppSensorMeta
from tcell_agent.appsensor.params import POST_PARAM
from tcell_agent.policies.appsensor_policy import AppSensorPolicy

class FakeFile(object):
    def __init__(self, filename):
        self.name = filename

class AppSensorPolicyCheckParamsTest(unittest.TestCase):


    def uploading_zero_file_test(self):
        policy = AppSensorPolicy()
        files_dict = MultiValueDict()
        meta = AppSensorMeta(
            "remote_addr",
            "request_method",
            "abosolute_uri",
            "route_id",
            session_id="session_id",
            user_id="user_id"
        )
        meta.request_data(1024, {}, {}, {}, '', 'user_agent', files_dict)

        with patch('tcell_agent.policies.appsensor_policy.safe_wrap_function') as patched_safe_wrap_function:
            policy.check_params_for_injections(meta, {})
            self.assertFalse(patched_safe_wrap_function.called)

    def uploading_one_file_test(self):
        policy = AppSensorPolicy()
        files_dict = MultiValueDict({'avatar': [FakeFile('potention_injection')]})
        meta = AppSensorMeta(
            "remote_addr",
            "request_method",
            "abosolute_uri",
            "route_id",
            session_id="session_id",
            user_id="user_id"
        )
        meta.request_data(1024, {}, {}, {}, '', 'user_agent', files_dict)

        with patch('tcell_agent.policies.appsensor_policy.safe_wrap_function') as patched_safe_wrap_function:
            policy.check_params_for_injections(meta, {})
            patched_safe_wrap_function.assert_called_once_with(
                'Check Filename injections',
                policy.check_param_for_injections,
                POST_PARAM,
                meta,
                'avatar',
                'potention_injection'
            )

    def uploading_two_files_for_same_param_test(self):
        policy = AppSensorPolicy()
        files_dict = MultiValueDict({
            'avatar': [FakeFile('potention_injection'), FakeFile('second_potention_injection')]
        })
        meta = AppSensorMeta(
            "remote_addr",
            "request_method",
            "abosolute_uri",
            "route_id",
            session_id="session_id",
            user_id="user_id"
        )
        meta.request_data(1024, {}, {}, {}, '', 'user_agent', files_dict)

        with patch('tcell_agent.policies.appsensor_policy.safe_wrap_function') as patched_safe_wrap_function:
            policy.check_params_for_injections(meta, {})
            patched_safe_wrap_function.assert_has_calls([
                call(
                    'Check Filename injections',
                    policy.check_param_for_injections,
                    POST_PARAM,
                    meta,
                    'avatar',
                    'potention_injection'),
                call(
                    'Check Filename injections',
                    policy.check_param_for_injections,
                    POST_PARAM,
                    meta,
                    'avatar',
                    'second_potention_injection')
            ], True)


    def uploading_two_files_for_different_params_test(self):
        policy = AppSensorPolicy()
        files_dict = MultiValueDict({
            'avatar': [FakeFile('potention_injection')],
            'picture': [FakeFile('second_potention_injection')]
            })
        meta = AppSensorMeta(
            "remote_addr",
            "request_method",
            "abosolute_uri",
            "route_id",
            session_id="session_id",
            user_id="user_id"
        )
        meta.request_data(1024, {}, {}, {}, '', 'user_agent', files_dict)

        with patch('tcell_agent.policies.appsensor_policy.safe_wrap_function') as patched_safe_wrap_function:
            policy.check_params_for_injections(meta, {})
            patched_safe_wrap_function.assert_has_calls(
                [
                    call(
                        'Check Filename injections',
                        policy.check_param_for_injections,
                        POST_PARAM,
                        meta,
                        'avatar',
                        'potention_injection'),
                    call(
                        'Check Filename injections',
                        policy.check_param_for_injections,
                        POST_PARAM,
                        meta,
                        'picture',
                        'second_potention_injection')
                ],
                True
            )
