import os

import pytest
import time

from python_agent.admin import cli
from python_agent.packages.click.testing import CliRunner
from python_agent.test_listener.agent_manager import AgentManager
from python_agent.test_listener.state_tracker import StateTracker
from python_agent.test_listener.utils import Singleton
from python_agent.tests.integration import utils


source_code_path = os.path.dirname(__file__) + "/revision1/calculator.py"
test_code_path = os.path.dirname(__file__) + "/revision1/calculator_test_pytest.py"


@pytest.fixture()
def agent_params():
    Singleton._instances.pop(AgentManager, None)
    Singleton._instances.pop(StateTracker, None)
    return {
        "customer_id": "integration",
        "app_name": "calculator",
        "server": "http://dev-shai8.sealights.co:8080/api",
        "env": "Integration Tests",
        "branch": "origin/master",
    }


def test_build_coverage(agent_params):
    build = utils.get_next_build_number(agent_params["customer_id"], agent_params["app_name"], agent_params["server"])
    print "Next Build Number: %s" % build

    runner = CliRunner()
    params = [
        "--customer_id", agent_params["customer_id"],
        "--app_name", agent_params["app_name"],
        "--server", agent_params["server"],
        "--source", source_code_path,
        "--env", agent_params["env"],
        "--branch", agent_params["branch"],
        "--build", build,
        "build"
    ]
    result = runner.invoke(cli, params)
    print "Finished Running Build. Params: %s" % params
    assert result.exit_code == 0

    params = [
        "--customer_id", agent_params["customer_id"],
        "--app_name", agent_params["app_name"],
        "--server", agent_params["server"],
        "--source", source_code_path,
        "--env", agent_params["env"],
        "--branch", agent_params["branch"],
        "--build", build,
        "pytest",
        "-vv", "-s",
        test_code_path
    ]
    result = runner.invoke(cli, params)
    print "Finished Running Tests. Params: %s" % params
    assert result.exit_code == 0

    time.sleep(60)

    build = utils.get_build(agent_params["customer_id"], agent_params["app_name"], agent_params["server"])
    print "Build After Tests: %s" % build
    assert build.get("coverage", {}).get("value") == 75
