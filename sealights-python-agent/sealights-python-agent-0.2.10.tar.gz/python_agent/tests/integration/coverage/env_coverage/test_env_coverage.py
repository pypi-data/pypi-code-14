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
test_code_path_env1 = os.path.dirname(__file__) + "/revision1/calculator_test_env1_pytest.py"
test_code_path_env2 = os.path.dirname(__file__) + "/revision1/calculator_test_env2_pytest.py"


@pytest.fixture()
def agent_params():
    Singleton._instances.pop(AgentManager, None)
    Singleton._instances.pop(StateTracker, None)
    return {
        "customer_id": "integration",
        "app_name": "calculator",
        "server": "http://dev-shai8.sealights.co:8080/api",
        "env1": "Unit Tests 1",
        "env2": "Unit Tests 2",
        "branch": "origin/master",
    }


def test_env_coverage(agent_params):
    build = utils.get_next_build_number(agent_params["customer_id"], agent_params["app_name"], agent_params["server"])
    print "Next Build Number: %s" % build

    runner = CliRunner()
    params = [
        "--customer_id", agent_params["customer_id"],
        "--app_name", agent_params["app_name"],
        "--server", agent_params["server"],
        "--source", source_code_path,
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
        "--env", agent_params["env1"],
        "--branch", agent_params["branch"],
        "--build", build,
        "pytest",
        "-vv", "-s",
        test_code_path_env1
    ]
    result = runner.invoke(cli, params)
    print "Finished Running Tests. Params: %s" % params
    assert result.exit_code == 0

    Singleton._instances.pop(AgentManager)
    Singleton._instances.pop(StateTracker)

    result = runner.invoke(cli, [
        "--customer_id", agent_params["customer_id"],
        "--app_name", agent_params["app_name"],
        "--server", agent_params["server"],
        "--source", source_code_path,
        "--env", agent_params["env2"],
        "--branch", agent_params["branch"],
        "--build", build,
        "pytest",
        "-vv", "-s",
        test_code_path_env2
    ])
    assert result.exit_code == 0

    time.sleep(60)

    build = utils.get_build(agent_params["customer_id"], agent_params["app_name"], agent_params["server"])
    print "Build After Tests: %s" % build
    environments = build.get("environments", [])

    assert environments
    assert len(environments) == 2

    for env in environments:
        if env["environmentName"] == agent_params["env1"]:
            assert env.get("coverage", {}).get("value") == 25
        if env["environmentName"] == agent_params["env2"]:
            assert env.get("coverage", {}).get("value") == 50
