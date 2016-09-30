import json
import re

from future.utils import iteritems
from tcell_agent.appsensor.params import GET_PARAM, POST_PARAM, JSON_PARAM, COOKIE_PARAM, URI_PARAM
from tcell_agent.appsensor.rules import rule_manager
from tcell_agent.config import CONFIGURATION
from tcell_agent.policies.appsensor.sensor import sendEvent
from tcell_agent.sensor_events import AppSensorEvent


class InjectionSensor(object):

    PARAM_TYPE_TO_L = {
        GET_PARAM: 'query',
        POST_PARAM: 'body',
        JSON_PARAM: 'body',
        URI_PARAM: 'uri',
        COOKIE_PARAM: 'cookie'
    }

    def __init__(self, dp, policy_json=None):
        self.enabled = False
        self.dp = dp
        self.exclude_headers = False
        self.exclude_forms = False
        self.exclude_cookies = False
        self.exclusions = {}
        self.active_pattern_ids = {}
        self.v1_compatability_enabled = False
        self.excluded_route_ids = {}

        if policy_json is not None:
            self.enabled = policy_json.get("enabled", False)
            self.exclude_headers = policy_json.get("exclude_headers", False)
            self.exclude_forms = policy_json.get("exclude_forms", False)
            self.exclude_cookies = policy_json.get("exclude_cookies", False)
            self.v1_compatability_enabled = policy_json.get("v1_compatability_enabled", False)

            for route_id in policy_json.get("exclude_routes", []):
                self.excluded_route_ids[route_id] = True

            for pattern in policy_json.get("patterns", []):
                self.active_pattern_ids[pattern] = True

            for common_word, locations in iteritems(policy_json.get("exclusions", {})):
                self.exclusions[common_word] = locations

    def check(self, type_of_param, appsensor_meta, param_name, param_value, payloads_policy):
        if not self.enabled:
            return False

        if self.excluded_route_ids.get(appsensor_meta.route_id, False):
            return False

        if self.exclude_forms and (GET_PARAM == type_of_param or POST_PARAM == type_of_param or JSON_PARAM == type_of_param):
            return False

        if self.exclude_cookies and COOKIE_PARAM == type_of_param:
            return False

        vuln_results = self.check_dp_violation(param_name, param_value)

        if vuln_results:
            vuln_param = vuln_results.get("param")

            if vuln_param:
                meta = {"l": self.PARAM_TYPE_TO_L[type_of_param]}
                pattern = vuln_results.get("pattern")

                payload = payloads_policy.apply(
                    self.dp,
                    appsensor_meta,
                    type_of_param,
                    vuln_param,
                    vuln_results.get("value"),
                    meta,
                    pattern
                )

                sendEvent(
                    appsensor_meta,
                    self.dp,
                    vuln_param,
                    meta,
                    payload,
                    pattern)

                return True

        return False

    def check_dp_violation(self, param_name, param_value):
        rules = self.get_ruleset()
        if rules:
            return rules.check_violation(param_name, param_value, self.active_pattern_ids, self.v1_compatability_enabled)
        return None

    def get_ruleset(self):
        return rule_manager.get_ruleset_for(self.dp)

    def __str__(self):
        return "<%s enabled: %s dp: %s exclude_headers: %s exclude_forms: %s exclude_cookies: %s v1_compatability_enabled: %s active_pattern_ids: %s exclusions: %s>" % \
            (type(self).__name__, self.enabled, self.dp, self.exclude_headers, self.exclude_forms, self.exclude_cookies, self.v1_compatability_enabled, self.active_pattern_ids, self.exclusions)
