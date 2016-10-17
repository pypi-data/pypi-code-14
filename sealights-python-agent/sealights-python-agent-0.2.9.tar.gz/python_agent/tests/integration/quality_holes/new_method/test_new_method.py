import os

import pytest
import time

from python_agent.admin import cli
from python_agent.packages.click.testing import CliRunner
from python_agent.test_listener.agent_manager import AgentManager
from python_agent.test_listener.state_tracker import StateTracker
from python_agent.test_listener.utils import Singleton
from python_agent.tests.integration import utils

title = "new method creates a quality hole"

revision1_source_code_path = os.path.dirname(__file__) + "/revision1"
revision2_source_code_path = os.path.dirname(__file__) + "/revision2"


@pytest.fixture()
def agent_params():
    return {
        "customer_id": "integration",
        "app_name": "calculator",
        "server": "http://dev-shai8.sealights.co:8080/api",
        "env": "Integration Tests",
        "branch": "origin/master",
    }


def test_quality_holes_new_method(agent_params):
    build1_num = utils.get_next_build_number(agent_params["customer_id"], agent_params["app_name"], agent_params["server"])
    print "Next Build Number: %s" % build1_num

    os.chdir(revision1_source_code_path)
    runner = CliRunner()
    params = [
        "--customer_id", agent_params["customer_id"],
        "--app_name", agent_params["app_name"],
        "--server", agent_params["server"],
        "--include", "*calculator.py",
        "--env", agent_params["env"],
        "--branch", agent_params["branch"],
        "--build", build1_num,
        "build"
    ]
    result = runner.invoke(cli, params)
    assert result.exit_code == 0
    print "Finished Running Build. Params: %s" % params

    Singleton._instances.pop(AgentManager)
    Singleton._instances.pop(StateTracker)

    params = [
        "--customer_id", agent_params["customer_id"],
        "--app_name", agent_params["app_name"],
        "--server", agent_params["server"],
        "--include", "*calculator.py",
        "--env", agent_params["env"],
        "--branch", agent_params["branch"],
        "--build", build1_num,
        "pytest",
        "-vv", "-s",
        revision1_source_code_path + "/calculator_test_pytest.py"
    ]
    result = runner.invoke(cli, params)
    assert result.exit_code == 0
    print "Finished Running Tests. Params: %s" % params

    Singleton._instances.pop(AgentManager)
    Singleton._instances.pop(StateTracker)

    time.sleep(60)

    build2_num = utils.bump_version(build1_num)
    print "Next Build Number: %s" % build2_num

    os.chdir(revision2_source_code_path)
    params = [
        "--customer_id", agent_params["customer_id"],
        "--app_name", agent_params["app_name"],
        "--server", agent_params["server"],
        "--include", "*calculator.py",
        "--env", agent_params["env"],
        "--branch", agent_params["branch"],
        "--build", build2_num,
        "build"
    ]
    result = runner.invoke(cli, params)
    assert result.exit_code == 0
    print "Finished Running Build. Params: %s" % params

    Singleton._instances.pop(AgentManager)
    Singleton._instances.pop(StateTracker)

    params = [
        "--customer_id", agent_params["customer_id"],
        "--app_name", agent_params["app_name"],
        "--server", agent_params["server"],
        "--include", "*calculator.py",
        "--env", agent_params["env"],
        "--branch", agent_params["branch"],
        "--build", build2_num,
        "pytest",
        "-vv", "-s",
        revision2_source_code_path + "/calculator_test_pytest.py"
    ]
    result = runner.invoke(cli, params)
    assert result.exit_code == 0
    print "Finished Running Tests. Params: %s" % params

    Singleton._instances.pop(AgentManager)
    Singleton._instances.pop(StateTracker)

    time.sleep(60)

    build2 = utils.get_build(agent_params["customer_id"], agent_params["app_name"], agent_params["server"])
    print "Build #2: %s" % build2
    environments = build2.get("environments", [])

    assert environments
    assert len(environments) == 1

    assert environments[0].get("qualityHoles", {}).get("newQh") == 1
