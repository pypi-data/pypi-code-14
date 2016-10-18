import logging
import operator
import os
from collections import defaultdict

from _pytest.hookspec import hookspec
from _pytest.junitxml import mangle_test_address
from python_agent import config

from python_agent.test_listener.agent_manager import AgentManager
from python_agent.test_listener.sealights_api import SeaLightsAPI

log = logging.getLogger(__name__)


class SealightsPlugin(object):
    def __init__(self):
        self.test_status = defaultdict(lambda: defaultdict(lambda: defaultdict(bool)))
        self.execution_id = SeaLightsAPI.create_execution_id()

    def pytest_sessionstart(self, session):
        try:
            SeaLightsAPI.notify_execution_start(self.execution_id)
        except Exception as e:
            log.exception("Failed Notifying Execution Start. Execution Id: %s. Error: %s" % (self.execution_id, str(e)))

    def pytest_sessionfinish(self, session, exitstatus):
        try:
            SeaLightsAPI.notify_execution_end(self.execution_id)
        except Exception as e:
            log.exception("Failed Notifying Execution End. Execution Id: %s. Error: %s" % (self.execution_id, str(e)))
        if os.environ.get("SL_TEST"):
            AgentManager().shutdown()

    def pytest_runtest_logstart(self, nodeid, location):
        try:
            SeaLightsAPI.notify_test_start(self.execution_id, get_test_name(nodeid))
        except Exception as e:
            log.exception("Failed Notifying Test Start. Full Test Name: %s. Error: %s" % (nodeid, str(e)))

    @hookspec(firstresult=True)
    def pytest_report_teststatus(self, report):
        try:
            self.test_status[report.nodeid]["passed"][report.when] = report.passed
            self.test_status[report.nodeid]["skipped"][report.when] = report.skipped
            self.test_status[report.nodeid]["failed"][report.when] = report.failed
            if report.when == "teardown":
                test = self.test_status[report.nodeid]
                passed = reduce(operator.and_, test["passed"].values())
                skipped = reduce(operator.or_, test["skipped"].values())
                failed = reduce(operator.or_, test["failed"].values())
                if passed:
                    SeaLightsAPI.notify_test_end(self.execution_id, get_test_name(report.nodeid), report.duration, "passed")
                elif skipped:
                    SeaLightsAPI.notify_test_end(self.execution_id, get_test_name(report.nodeid), report.duration, "skipped")
                elif failed:
                    SeaLightsAPI.notify_test_end(self.execution_id, get_test_name(report.nodeid), report.duration, "failed")
        except Exception as e:
            log.exception("Failed Notifying Test End, Skip or Failed. Full Test Name: %s. Error: %s"
                          % (report.nodeid, str(e)))

    def pytest_internalerror(excrepr, excinfo):
        log.exception("Test Internal Error. Exception: %s. Excinfo: %s" % (excrepr, excinfo))

    def pytest_exception_interact(node, call, report):
        log.exception("Test Exception. Node: %s. Call: %s. Report: %s" % (node, call, report))


def context_match(frame):
    # regular pytest tests
    if hasattr(frame, "f_back") and hasattr(frame.f_back, "f_locals") and "pyfuncitem" in frame.f_back.f_locals.keys():
        return get_test_name(getattr(frame.f_back.f_locals["pyfuncitem"], "nodeid"))

    # pytest running unittest tests
    if hasattr(frame, "f_locals") and "self" in frame.f_locals.keys() and \
        hasattr(frame.f_locals["self"], "_resultForDoCleanups") and \
        hasattr(frame.f_locals["self"]._resultForDoCleanups, "nodeid"):
            return get_test_name(frame.f_locals["self"]._resultForDoCleanups.nodeid)


def get_test_name(nodeid):
    # Parametrized tests can be very long.
    # We account it as a single test
    node_id = nodeid.split("[")[0]
    if config.app["test_phase"]:
        node_id = ".".join(mangle_test_address(node_id))
    return node_id
