# -*- coding: utf-8 -*-
# Copyright (C) 2015 tCell.io, Inc. - All Rights Reserved

from future.utils import iteritems
from tcell_agent.appsensor import params
from tcell_agent.appsensor.params import GET_PARAM, POST_PARAM, JSON_PARAM, COOKIE_PARAM, URI_PARAM
from tcell_agent.config import CONFIGURATION
from tcell_agent.instrumentation import safe_wrap_function
from tcell_agent.policies import TCellPolicy
from tcell_agent.policies.appsensor import CmdiSensor
from tcell_agent.policies.appsensor import DatabaseSensor
from tcell_agent.policies.appsensor import FptSensor
from tcell_agent.policies.appsensor import LoginSensor
from tcell_agent.policies.appsensor import MiscSensor
from tcell_agent.policies.appsensor import NullbyteSensor
from tcell_agent.policies.appsensor import RequestSizeSensor
from tcell_agent.policies.appsensor import ResponseCodesSensor
from tcell_agent.policies.appsensor import ResponseSizeSensor
from tcell_agent.policies.appsensor import RetrSensor
from tcell_agent.policies.appsensor import SqliSensor
from tcell_agent.policies.appsensor import UserAgentSensor
from tcell_agent.policies.appsensor import XssSensor
from tcell_agent.policies.appsensor import PayloadsPolicy

class AppSensorPolicy(TCellPolicy):
    api_identifier = "appsensor"

    options = [
        "req_res_size",
        "resp_codes",
        "xss",
        "sqli",
        "cmdi",
        "fpt",
        "null",
        "retr",
        "login_failure",
        "ua",
        "errors",
        "database"]

    options_v2_classes = {
        "req_size": RequestSizeSensor,
        "resp_size": ResponseSizeSensor,
        "resp_codes": ResponseCodesSensor,
        "xss": XssSensor,
        "sqli": SqliSensor,
        "cmdi": CmdiSensor,
        "fpt": FptSensor,
        "nullbyte": NullbyteSensor,
        "retr": RetrSensor,
        "login": LoginSensor,
        "ua": UserAgentSensor,
        "errors": MiscSensor,
        "database": DatabaseSensor}

    def __init__(self, policy_json=None):
        super(AppSensorPolicy, self).__init__()
        self.init_variables()
        if policy_json is not None:
            self.loadFromJson(policy_json)

    def init_variables(self):
        self.enabled = False
        self.payloads_policy = PayloadsPolicy()
        self.options = {}

    def run_for_request(self, appsensor_meta, json_body):
        self.check_request_size(appsensor_meta)

        self.check_params_for_injections(appsensor_meta, json_body)

        if "ua" in self.options:
            safe_wrap_function(
                "Check User Agent",
                self.options["ua"].check,
                appsensor_meta
            )


    def run_for_response(self, appsensor_meta):
        self.check_response_size(appsensor_meta)
        self.check_response_code(appsensor_meta)

    def run_for_path_parameters(self, appsensor_meta):
        path_dict = appsensor_meta.path_dict

        for param_name, param_value in iteritems(path_dict or {}):
            safe_wrap_function(
                "Check PATH var injections",
                self.check_param_for_injections,
                URI_PARAM,
                appsensor_meta,
                param_name,
                param_value
            )


    def check_login_failure(self, appsensor_meta, username):
        if "login" in self.options:
            safe_wrap_function(
                "Check Login Failure",
                self.options["login"].check,
                appsensor_meta,
                username
            )

    def check_db_rows(self, appsensor_meta, number_of_records):
        if "database" in self.options:
            safe_wrap_function(
                "Appsensor Check Number of DB Rows",
                self.options["database"].check,
                appsensor_meta,
                number_of_records
            )

    def check_param_for_injections(self, param_type, appsensor_meta, param_name, param_value):
        if self.options.get("xss") and self.options["xss"].check(param_type, appsensor_meta, param_name, param_value, self.payloads_policy):
            return
        if self.options.get("sqli") and self.options["sqli"].check(param_type, appsensor_meta, param_name, param_value, self.payloads_policy):
            return
        if COOKIE_PARAM != param_type:
            if self.options.get("cmdi") and self.options["cmdi"].check(param_type, appsensor_meta, param_name, param_value, self.payloads_policy):
                return
        if COOKIE_PARAM != param_type:
            if self.options.get("fpt") and self.options["fpt"].check(param_type, appsensor_meta, param_name, param_value, self.payloads_policy):
                return
        if COOKIE_PARAM != param_type:
            if self.options.get("nullbyte") and self.options["nullbyte"].check(param_type, appsensor_meta, param_name, param_value, self.payloads_policy):
                return
        if GET_PARAM == param_type or COOKIE_PARAM == param_type:
            if self.options.get("retr") and self.options["retr"].check(param_type, appsensor_meta, param_name, param_value, self.payloads_policy):
                return

    def check_params_for_injections(self, appsensor_meta, json_body):
        get_dict = params.flatten_clean(appsensor_meta.get_dict)
        cookie_dict = params.flatten_clean(appsensor_meta.cookie_dict)
        json_body = params.flatten_clean(json_body)

        post_dict = appsensor_meta.post_dict
        files_dict = appsensor_meta.files_dict

        for param_name, param_value in iteritems(get_dict):
            param_name = param_name[-1]
            safe_wrap_function(
                "Check GET var injections",
                self.check_param_for_injections,
                GET_PARAM,
                appsensor_meta,
                param_name,
                param_value
            )

        for param_name, param_value in iteritems(post_dict):
            param_name = param_name[-1]
            safe_wrap_function(
                "Check POST var injections",
                self.check_param_for_injections,
                POST_PARAM,
                appsensor_meta,
                param_name,
                param_value
            )

        for param_name, param_value in iteritems(files_dict):
            param_name = param_name[-1]
            safe_wrap_function(
                "Check Filename injections",
                self.check_param_for_injections,
                POST_PARAM,
                appsensor_meta,
                param_name,
                param_value
            )

        for param_name, param_value in iteritems(cookie_dict or {}):
            param_name = param_name[-1]
            safe_wrap_function(
                "Check Cookies var injections",
                self.check_param_for_injections,
                COOKIE_PARAM,
                appsensor_meta,
                param_name,
                param_value
            )

        for param_name, param_value in iteritems(json_body or {}):
            param_name = param_name[-1]
            safe_wrap_function(
                "Check JSON var injections",
                self.check_param_for_injections,
                JSON_PARAM,
                appsensor_meta,
                param_name,
                param_value
            )


    def check_request_size(self, appsensor_meta):
        if "req_size" in self.options:
            safe_wrap_function(
                "Check Request Size",
                self.options["req_size"].check,
                appsensor_meta,
                appsensor_meta.request_content_len)

    def check_response_size(self, appsensor_meta):
        if "resp_size" in self.options:
            safe_wrap_function(
                "Check Response Size",
                self.options["resp_size"].check,
                appsensor_meta,
                appsensor_meta.response_content_len)

    def check_response_code(self, appsensor_meta):
        if "resp_codes" in self.options:
            safe_wrap_function(
                "Check Response Codes",
                self.options["resp_codes"].check,
                appsensor_meta,
                appsensor_meta.response_code)

    def csrf_rejected(self, appsensor_meta, reason):
        if "errors" in self.options:
            safe_wrap_function(
                "CSRF Exception processing",
                self.options["errors"].csrf_rejected,
                appsensor_meta,
                reason)

    def sql_exception_detected(self, database, appsensor_meta, exc_type, exc_value, traceback):
        if "errors" in self.options:
            safe_wrap_function(
                "SQL Exception processing",
                self.options["errors"].sql_exception_detected,
                database,
                appsensor_meta,
                exc_type,
                exc_value,
                traceback)

    def loadFromJson(self, policy_json):
        if "policy_id" in policy_json:
            self.policy_id = policy_json["policy_id"]
        else:
            raise Exception("Policy Id Not Found")

        self.init_variables()

        policy_data = policy_json.get("data")

        if "version" in policy_json and policy_json["version"] == 2:
            if policy_data:
                sensors_json = policy_data.get("sensors")
                if sensors_json:
                    self.payloads_policy.from_json(policy_data.get("options", {}))

                    for option, clazz in iteritems(self.options_v2_classes):
                        settings = sensors_json.get(option, {})
                        settings["enabled"] = option in sensors_json
                        self.options[option] = clazz(settings)

        else:
            if policy_data:
                options_json = policy_data.get("options")
                if options_json:
                    self.payloads_policy.from_json({
                        "payloads": {
                            "send_payloads": True,
                            "log_payloads": True
                        }
                    })

                    for option in AppSensorPolicy.options:
                        if "req_res_size" == option:
                            enabled = options_json.get(option, False)
                            self.options["req_size"] = RequestSizeSensor({"enabled": enabled})
                            self.options["resp_size"] = ResponseSizeSensor({"enabled": enabled})
                        elif "resp_codes" == option:
                            enabled = options_json.get(option, False)
                            self.options[option] = ResponseCodesSensor({
                                "enabled": enabled,
                                "series_400_enabled": True,
                                "series_500_enabled": True})
                        elif "null"  == option:
                            enabled = options_json.get(option, False)
                            self.options["nullbyte"] = NullbyteSensor({"enabled": enabled, "v1_compatability_enabled": True})
                        elif "login_failure"  == option:
                            enabled = options_json.get(option, False)
                            self.options["login"] = LoginSensor({"enabled": enabled})
                        elif "ua" == option:
                            self.options[option] = UserAgentSensor({"enabled": False, "empty_enabled": False})
                        elif "errors" == option:
                            self.options[option] = MiscSensor({"csrf_exception_enabled": False, "sql_exception_enabled": False})
                        else:
                            enabled = options_json.get(option, False)
                            clazz = self.options_v2_classes[option]
                            self.options[option] = clazz({"enabled": enabled, "v1_compatability_enabled": True})
