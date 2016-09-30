import json

from future.utils import iteritems

from tcell_agent.appsensor.params import GET_PARAM, POST_PARAM, JSON_PARAM, COOKIE_PARAM, URI_PARAM
from tcell_agent.config import CONFIGURATION
from tcell_agent.sensor_events import AppSensorEvent

# set is builtin in python 3 but a module in earlier version
try:
    set
except NameError:
    from sets import Set as set

import logging
PAYLOADS_LOGGER = logging.getLogger('app_firewall_payloads_logger').getChild(__name__)

def get_payloads_logger():
    return PAYLOADS_LOGGER

class PayloadsPolicy(object):

    DEFAULT_BLACKLIST = {
        "token": set(['*']),
        "client_secret": set(['*']),
        "password": set(['*']),
        "passwd": set(['*']),
        "refresh_token": set(['*']),
        "pf.pass": set(['*']),
        "user.password": set(['*']) }

    PARAM_TYPE_MAP = {
        GET_PARAM: "form",
        POST_PARAM: "form",
        JSON_PARAM: "form",
        URI_PARAM: "form",
        COOKIE_PARAM: "cookie" }


    def __init__(self, policy_json=None):
        self.reset()

    def reset(self):
        self.send_payloads = False
        self.send_payloads = False
        self.log_payloads = False

        self.send_blacklist = self.DEFAULT_BLACKLIST
        self.log_blacklist = self.DEFAULT_BLACKLIST
        self.send_whitelist = {}
        self.log_whitelist = {}

        self.use_send_whitelist = False
        self.use_log_whitelist = False

    def apply(self, dp, appsensor_meta, type_of_param, vuln_param, vuln_value, meta, pattern):
        payload = None

        if self.send_payloads and CONFIGURATION.allow_unencrypted_appsensor_payloads:

            blacklisted_locations = self.send_blacklist.get(vuln_param.lower(), None)
            param_location = self.PARAM_TYPE_MAP[type_of_param]

            if blacklisted_locations and ( param_location in blacklisted_locations or "*" in blacklisted_locations ):
                payload = "BLACKLISTED"

            elif self.use_send_whitelist:
                whitelisted_locations = self.send_whitelist.get(vuln_param.lower(), None)
                if whitelisted_locations and ( param_location in whitelisted_locations or "*" in whitelisted_locations ):
                  payload = vuln_value

                else:
                  payload = "NOT_WHITELISTED"

            else:
              payload = vuln_value


        self.log(dp, appsensor_meta, type_of_param, vuln_param, vuln_value, meta, pattern)

        return payload

    def log(self, dp, appsensor_meta, type_of_param, vuln_param, vuln_value, meta, pattern):
        if self.log_payloads and CONFIGURATION.log_appfirewall_events:
            blacklisted_locations = self.log_blacklist.get(vuln_param.lower(), None)
            param_location = self.PARAM_TYPE_MAP[type_of_param]

            if blacklisted_locations is None or \
                ( param_location not in blacklisted_locations and "*" not in blacklisted_locations ):

                whitelisted_locations = self.log_whitelist.get(vuln_param.lower(), None)
                if not self.use_log_whitelist or \
                    ( whitelisted_locations is not None and \
                    ( param_location in whitelisted_locations or "*" in whitelisted_locations ) ):

                    event = AppSensorEvent(dp,
                        vuln_param,
                        appsensor_meta.location,
                        appsensor_meta.remote_address,
                        appsensor_meta.route_id,
                        meta,
                        appsensor_meta.method,
                        payload=vuln_value,
                        user_id=appsensor_meta.user_id,
                        hmacd_session_id=appsensor_meta.session_id,
                        pattern=pattern)

                    get_payloads_logger().info(json.dumps(event))

    def from_json(self, policy_json):
        self.reset()

        if policy_json:
            payloads_json = policy_json.get("payloads", {})
            self.send_payloads = payloads_json.get("send_payloads", False)
            self.log_payloads = payloads_json.get("log_payloads", False)

            if self.send_payloads:
                send_blacklist = payloads_json.get("send_blacklist", None)
                if send_blacklist is not None:
                    self.send_blacklist = {}
                    for param_name, locations in iteritems(payloads_json.get("send_blacklist", {})):
                        self.send_blacklist[param_name.lower()] = set(locations)

                send_whitelist = payloads_json.get("send_whitelist", None)
                if send_whitelist is not None:
                    for param_name, locations in iteritems(send_whitelist):
                        self.send_whitelist[param_name.lower()] = set(locations)

                    self.use_send_whitelist = True

            if self.log_payloads:
                log_blacklist = payloads_json.get("log_blacklist", None)
                if log_blacklist is not None:
                    self.log_blacklist = {}
                    for param_name, locations in iteritems(payloads_json.get("log_blacklist", {})):
                        self.log_blacklist[param_name.lower()] = set(locations)

                log_whitelist = payloads_json.get("log_whitelist", None)
                if log_whitelist is not None:
                    for param_name, locations in iteritems(log_whitelist):
                        self.log_whitelist[param_name.lower()] = set(locations)
                    self.use_log_whitelist = True
