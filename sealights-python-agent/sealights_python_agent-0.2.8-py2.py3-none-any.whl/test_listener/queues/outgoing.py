import logging
import os
import platform
import socket

import pkg_resources

from python_agent import config
from python_agent.packages import requests
from python_agent.test_listener.utils import StateTracker

log = logging.getLogger(__name__)


class OutgoingMessageQueue(object):

    def __init__(self, customer_id, app_name, build, branch, env, server):
        self.customer_id = customer_id
        self.app_name = app_name
        self.build = build
        self.branch = branch
        self.env = env
        self.server = server

    def test_started(self, test_name, example_group, execution_id):
        event = {
            "type": "testStart",
            "testName": test_name,
            "suitPath": example_group,
            "executionId": execution_id
        }
        self.send_event(event)

    def test_passed(self, test_name, example_group, execution_id, duration):
        event = {
            "type": "testEnd",
            "testName": test_name,
            "suitPath": example_group,
            "executionId": execution_id,
            "result": "passed",
            "duration": duration
        }
        self.send_event(event)

    def test_failed(self, test_name, example_group, execution_id, duration):
        event = {
            "type": "testEnd",
            "testName": test_name,
            "suitPath": example_group,
            "executionId": execution_id,
            "result": "failed",
            "duration": duration
        }
        self.send_event(event)

    def test_skipped(self, test_name, example_group, execution_id, duration):
        event = {
            "type": "testEnd",
            "testName": test_name,
            "suitPath": example_group,
            "executionId": execution_id,
            "result": "skipped",
            "duration": duration
        }
        self.send_event(event)

    def execution_started(self, execution_id):
        event = {
            "type": "executionIdStarted",
            "framework": "python",
            "executionId": execution_id
        }
        self.send_event(event)

    def execution_ended(self, execution_id):
        event = {
            "type": "executionIdEnded",
            "executionId": execution_id
        }
        self.send_event(event)

    def send_event(self, event):
        url = None
        try:
            message = {}
            message["appName"] = self.app_name
            message["customerId"] = self.customer_id
            message["environment"] = self.create_environment()
            message["events"] = [event]
            if self.branch:
                message["branch"] = self.branch
            if self.build:
                message["build"] = self.build

            url = self.server + "/v1/testevents"

            response = requests.post(
                url,
                json=message,
                headers={config.TEST_IDENTIFIER: StateTracker().current_test_identifier}
            )
            response.raise_for_status()
        except Exception as e:
            log.exception("failed sending event. url: %s. event: %s. error:%s" % (url, event, str(e)))

    def create_environment(self):
        try:
            return {
                "agentType": "python",
                "agentVersion": pkg_resources.require("sealights-python-agent")[0].version,
                "environmentName": self.env,
                "machineName": socket.gethostname(),
                "platform": platform.system(),
                "os": platform.system(),
                "osVersion": platform.release(),
                "arch": platform.machine(),
                "processId": os.getpid(),
                "dependencies": dict((package_name, pkg_resources.require(package_name)[0].version)
                                     for package_name, class_name in pkg_resources.working_set.by_key.items()),
                "compiler": platform.python_compiler(),
                "interpreter": platform.python_implementation(),
                "runtime": platform.python_version(),
                "configuration": config.app
            }
        except Exception as e:
            log.exception("failed to create environment. error: %s" % str(e))
        return {
            "agentType": "python",
            "agentVersion": "",
            "environmentName": self.env,
            "configuration": config.app
        }
