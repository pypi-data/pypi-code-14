import pytest
from mock import ANY

from python_agent import config
from python_agent.packages import semantic_version
from python_agent.test_listener.sealights_api import SeaLightsAPI
from python_agent.utils.autoupgrade import AutoUpgrade

pytest_plugins = "pytester"
config.INTERVAL_IN_MILLISECONDS = 50


@pytest.fixture(scope="function", autouse=True)
def mocks(mocker):
    mock_pkg = mocker.patch("pkg_resources.get_distribution", spec=True)
    mock_pkg.return_value.version = "0.1.1"
    return {
        "mock_get": mocker.patch("python_agent.packages.requests.get", spec=True),
        "mock_post": mocker.patch("python_agent.packages.requests.post", spec=True),
        "mock_pkg": mock_pkg,
        "mock_upgrade_install": mocker.patch("python_agent.utils.autoupgrade.AutoUpgrade.install")
    }


@pytest.fixture(scope="function", autouse=True)
def agent_params(mocker):
    mock_pkg = mocker.patch("pkg_resources.get_distribution", spec=True)
    mock_pkg.return_value.version = "0.1.1"
    return {
        "customer_id": "customer",
        "app_name": "agent",
        "server": "http://someserver/api",
        "mock_get": mocker.patch("python_agent.packages.requests.get", spec=True),
        "mock_post": mocker.patch("python_agent.packages.requests.post", spec=True),
        "mock_pkg": mock_pkg,
        "mock_upgrade_install": mocker.patch("python_agent.utils.autoupgrade.AutoUpgrade.install")
    }


def test_sanity(testdir, agent_params, mocker, mocks):
    event_types = ['executionIdStarted', 'testStart', 'testEnd', 'testStart', 'testEnd', 'executionIdEnded']
    testdir.makepyfile(
        """
        def test_selenium_3plus3():
            assert 3+3 == 6

        def test_selenium_1plus1():
            assert 1+1 == 2
        """
    )
    mocker.patch("python_agent.init.upgrade_agent", autospec=True)
    result = testdir.runpytest(*[
        "--verbose",
        "-p",
        "python_agent.test_listener.integrations.pytest_helper",
        "-p",
        "no:sealights-python-agent",
        "--customer_id=%s" % agent_params["customer_id"],
        "--app_name=%s" % agent_params["app_name"],
        "--server=%s" % agent_params["server"]
    ])
    all_events = []
    for (args, kwargs) in mocks["mock_post"].call_args_list:
        assert args[0] == agent_params["server"] + "/v1/testevents"
        message = kwargs.get("json", {})
        assert message.get("customerId", "") == agent_params["customer_id"]
        assert message.get("appName", "") == agent_params["app_name"]
        assert message.get("branch", "") == "master"
        assert message.get("build", "") == "1"
        events = message.get("events", [])
        assert events
        all_events.extend(events)
    assert len(all_events) == 6
    assert sorted(map(lambda event: event.get("type"), all_events)) == sorted(event_types)

    result.assert_outcomes(passed=2)


def test_pass_skip(testdir, agent_params, mocker, mocks):
    testdir.makepyfile(
        """
        import pytest

        def test_selenium_3plus3():
            assert 3+3 == 6

        @pytest.mark.skip()
        def test_selenium_1plus1():
            assert 1+1 == 2
        """
    )
    mocker.patch("python_agent.init.upgrade_agent", autospec=True)
    result = testdir.runpytest(*[
        "--verbose",
        "-p",
        "python_agent.test_listener.integrations.pytest_helper",
        "-p",
        "no:sealights-python-agent",
        "--customer_id=%s" % agent_params["customer_id"],
        "--app_name=%s" % agent_params["app_name"],
        "--server=%s" % agent_params["server"]
    ])
    all_events = []
    for (args, kwargs) in mocks["mock_post"].call_args_list:
        message = kwargs.get("json", {})
        events = message.get("events", [])
        assert events
        all_events.extend(events)
    assert len(all_events) == 6
    for event in all_events:
        if "test_selenium_3plus3" in event.get("testName", "") and event.get("type") == "testEnd":
            assert event.get("result") == "passed"
        if "test_selenium_1plus1" in event.get("testName", "") and event.get("type") == "testEnd":
            assert event.get("result") == "skipped"

    result.assert_outcomes(passed=1, skipped=1)


def test_all_skipped(testdir, agent_params, mocker, mocks):
    testdir.makepyfile(
        """
        import pytest

        @pytest.mark.skip()
        def test_selenium_3plus3():
            assert 3+3 == 6

        @pytest.mark.skip()
        def test_selenium_1plus1():
            assert 1+1 == 2
        """
    )
    mocker.patch("python_agent.init.upgrade_agent", autospec=True)
    result = testdir.runpytest(*[
        "--verbose",
        "-p",
        "python_agent.test_listener.integrations.pytest_helper",
        "-p",
        "no:sealights-python-agent",
        "--customer_id=%s" % agent_params["customer_id"],
        "--app_name=%s" % agent_params["app_name"],
        "--server=%s" % agent_params["server"]
    ])
    all_events = []
    for (args, kwargs) in mocks["mock_post"].call_args_list:
        message = kwargs.get("json", {})
        events = message.get("events", [])
        assert events
        all_events.extend(events)
    assert len(all_events) == 6
    for event in all_events:
        if event.get("type") == "testEnd":
            assert event.get("result") == "skipped"

    result.assert_outcomes(skipped=2)


def test_skip_error(testdir, agent_params, mocker, mocks):
    testdir.makepyfile(
        """
        import pytest

        @pytest.mark.skip()
        def test_selenium_3plus3():
            assert 3+3 == 6

        def test_selenium_1plus1():
            a[1]
            assert 1+1 == 2
        """
    )
    mocker.patch("python_agent.init.upgrade_agent", autospec=True)
    result = testdir.runpytest(*[
        "--verbose",
        "-p",
        "python_agent.test_listener.integrations.pytest_helper",
        "-p",
        "no:sealights-python-agent",
        "--customer_id=%s" % agent_params["customer_id"],
        "--app_name=%s" % agent_params["app_name"],
        "--server=%s" % agent_params["server"]
    ])
    all_events = []
    for (args, kwargs) in mocks["mock_post"].call_args_list:
        message = kwargs.get("json", {})
        events = message.get("events", [])
        assert events
        all_events.extend(events)
    assert len(all_events) == 6
    for event in all_events:
        if "test_selenium_3plus3" in event.get("testName", "") and event.get("type") == "testEnd":
            assert event.get("result") == "skipped"
        if "test_selenium_1plus1" in event.get("testName", "") and event.get("type") == "testEnd":
            assert event.get("result") == "failed"

    result.assert_outcomes(failed=1, skipped=1)


def test_execution_start_fail(testdir, agent_params, mocker, mocks):
    event_types = ['testStart', 'testEnd', 'testStart', 'testEnd', 'executionIdEnded']
    testdir.makepyfile(
        """
        def test_selenium_3plus3():
            assert 3+3 == 6

        def test_selenium_1plus1():
            assert 1+1 == 2
        """
    )
    mock_start = mocker.patch.object(SeaLightsAPI, "notify_execution_start")
    mock_start.side_effect = Exception()
    mocker.patch("python_agent.init.upgrade_agent", autospec=True)
    result = testdir.runpytest(*[
        "--verbose",
        "-p",
        "python_agent.test_listener.integrations.pytest_helper",
        "-p",
        "no:sealights-python-agent",
        "--customer_id=%s" % agent_params["customer_id"],
        "--app_name=%s" % agent_params["app_name"],
        "--server=%s" % agent_params["server"]
    ])
    all_events = []
    for (args, kwargs) in mocks["mock_post"].call_args_list:
        message = kwargs.get("json", {})
        events = message.get("events", [])
        assert events
        all_events.extend(events)
    assert len(all_events) == 5
    assert sorted(map(lambda event: event.get("type"), all_events)) == sorted(event_types)

    result.assert_outcomes(passed=2)


def test_test_start_fail(testdir, agent_params, mocker, mocks):
    event_types = ['executionIdStarted', 'testEnd', 'testEnd', 'executionIdEnded']
    testdir.makepyfile(
        """
        def test_selenium_3plus3():
            assert 3+3 == 6

        def test_selenium_1plus1():
            assert 1+1 == 2
        """
    )
    mocker.patch("python_agent.init.upgrade_agent", autospec=True)
    mock_start_test = mocker.patch.object(SeaLightsAPI, "notify_test_start")
    mock_start_test.side_effect = Exception()
    result = testdir.runpytest(*[
        "--verbose",
        "-p",
        "python_agent.test_listener.integrations.pytest_helper",
        "-p",
        "no:sealights-python-agent",
        "--customer_id=%s" % agent_params["customer_id"],
        "--app_name=%s" % agent_params["app_name"],
        "--server=%s" % agent_params["server"]
    ])
    all_events = []
    for (args, kwargs) in mocks["mock_post"].call_args_list:
        message = kwargs.get("json", {})
        events = message.get("events", [])
        assert events
        all_events.extend(events)
    assert len(all_events) == 4
    assert sorted(map(lambda event: event.get("type"), all_events)) == sorted(event_types)

    result.assert_outcomes(passed=2)


def test_passed_test_fail(testdir, agent_params, mocker, mocks):
    event_types = ['executionIdStarted', 'testStart', 'testStart', 'executionIdEnded']
    testdir.makepyfile(
        """
        def test_selenium_3plus3():
            assert 3+3 == 6

        def test_selenium_1plus1():
            assert 1+1 == 2
        """
    )
    mocker.patch("python_agent.init.upgrade_agent", autospec=True)
    mock_passed_test = mocker.patch.object(SeaLightsAPI, "notify_test_end")
    mock_passed_test.side_effect = Exception()
    result = testdir.runpytest(*[
        "--verbose",
        "-p",
        "python_agent.test_listener.integrations.pytest_helper",
        "-p",
        "no:sealights-python-agent",
        "--customer_id=%s" % agent_params["customer_id"],
        "--app_name=%s" % agent_params["app_name"],
        "--server=%s" % agent_params["server"]
    ])
    all_events = []
    for (args, kwargs) in mocks["mock_post"].call_args_list:
        message = kwargs.get("json", {})
        events = message.get("events", [])
        assert events
        all_events.extend(events)
    assert len(all_events) == 4
    assert sorted(map(lambda event: event.get("type"), all_events)) == sorted(event_types)

    result.assert_outcomes(passed=2)


def test_skipped_test_fail(testdir, agent_params, mocker, mocks):
    event_types = ['executionIdStarted', 'testStart', 'testStart', 'executionIdEnded']
    testdir.makepyfile(
        """
        import pytest

        def test_3plus3():
            assert 3+3 == 6

        @pytest.mark.skip()
        def test_1plus1():
            assert 1+1 == 2
        """
    )
    mocker.patch("python_agent.init.upgrade_agent", autospec=True)
    mock_skipped_test = mocker.patch.object(SeaLightsAPI, "notify_test_end")
    mock_skipped_test.side_effect = Exception()
    result = testdir.runpytest(*[
        "--verbose",
        "-p",
        "python_agent.test_listener.integrations.pytest_helper",
        "-p",
        "no:sealights-python-agent",
        "--customer_id=%s" % agent_params["customer_id"],
        "--app_name=%s" % agent_params["app_name"],
        "--server=%s" % agent_params["server"]
    ])
    all_events = []
    for (args, kwargs) in mocks["mock_post"].call_args_list:
        message = kwargs.get("json", {})
        events = message.get("events", [])
        assert events
        all_events.extend(events)
    assert len(all_events) == 4
    assert sorted(map(lambda event: event.get("type"), all_events)) == sorted(event_types)

    mock_skipped_test.assert_any_call(ANY, ANY, ANY, "passed")
    mock_skipped_test.assert_any_call(ANY, ANY, ANY, "skipped")

    result.assert_outcomes(passed=1, skipped=1)


def test_failed_test_fail(testdir, agent_params, mocker, mocks):
    testdir.makepyfile(
        """
        import pytest

        def test_3plus3():
            assert 3+3 == 6

        def test_1plus1():
            a[1]
            assert 1+1 == 2
        """
    )
    mocker.patch("python_agent.init.upgrade_agent", autospec=True)
    mock_failed_test = mocker.patch.object(SeaLightsAPI, "notify_test_end")
    mock_failed_test.side_effect = Exception()
    result = testdir.runpytest(*[
        "--verbose",
        "-p",
        "python_agent.test_listener.integrations.pytest_helper",
        "-p",
        "no:sealights-python-agent",
        "--customer_id=%s" % agent_params["customer_id"],
        "--app_name=%s" % agent_params["app_name"],
        "--server=%s" % agent_params["server"]
    ])
    all_events = []
    for (args, kwargs) in mocks["mock_post"].call_args_list:
        message = kwargs.get("json", {})
        events = message.get("events", [])
        assert events
        all_events.extend(events)
    assert len(all_events) == 4
    mock_failed_test.assert_any_call(ANY, ANY, ANY, "passed")
    mock_failed_test.assert_any_call(ANY, ANY, ANY, "failed")

    result.assert_outcomes(failed=1, passed=1)


def test_config_server(testdir, agent_params, mocker, mocks):
    testdir.makepyfile(
        """
        import pytest

        def test_selenium_3plus3():
            assert 3+3 == 6

        @pytest.mark.skip()
        def test_selenium_1plus1():
            assert 1+1 == 2
        """
    )
    mocker.patch.dict('python_agent.config.app', spec=True, wraps=config.app)
    mock_upgrade = mocker.patch.object(AutoUpgrade, "upgrade")
    mock_upgrade.return_value = 1
    mock_response = mocker.patch('python_agent.packages.requests.Response')
    mock_response.json.return_value = {
        'meta': {
            'query': 'Python',
            'generated': '2016-08-29T14:33:34.852Z',
            'version': '1.7.265',
            'customerId': 'nutanix'
        },
        'config': '{"featuresData.enableSendLogs":true}'
    }
    mocks["mock_get"].return_value = mock_response
    result = testdir.runpytest(*[
        "--verbose",
        "-p",
        "python_agent.test_listener.integrations.pytest_helper",
        "-p",
        "no:sealights-python-agent",
        "--customer_id=%s" % agent_params["customer_id"],
        "--app_name=%s" % agent_params["app_name"],
        "--server=%s" % agent_params["server"]
    ])
    assert config.app.get("featuresData.enableSendLogs") is True
    assert mocks["mock_get"].call_count == 1
    result.assert_outcomes(passed=1, skipped=1)


def test_autoupgrade_same_version(testdir, agent_params, mocker, mocks):
    testdir.makepyfile(
        """
        def test_3plus3():
            assert 3+3 == 6

        def test_1plus1():
            assert 1+1 == 2
        """
    )
    mocks["mock_upgrade_install"].return_value = 1
    mock_current_version = mocker.patch.object(AutoUpgrade, "get_current_version")
    mock_current_version.return_value = semantic_version.Version("0.1.1")
    mock_recommended_version = mocker.patch.object(AutoUpgrade, "get_recommended_version")
    mock_recommended_version.return_value = semantic_version.Version("0.1.1")
    result = testdir.runpytest(*[
        "--verbose",
        "-p",
        "python_agent.test_listener.integrations.pytest_helper",
        "-p",
        "no:sealights-python-agent",
        "--customer_id=%s" % agent_params["customer_id"],
        "--app_name=%s" % agent_params["app_name"],
        "--server=%s" % agent_params["server"]
    ])
    assert not mocks["mock_upgrade_install"].called
    result.assert_outcomes(passed=2)


def test_autoupgrade_newer_version(testdir, agent_params, mocker, mocks):
    testdir.makepyfile(
        """
        def test_3plus3():
            assert 3+3 == 6

        def test_1plus1():
            assert 1+1 == 2
        """
    )
    mocks["mock_upgrade_install"].return_value = 0
    mock_current_version = mocker.patch.object(AutoUpgrade, "get_current_version")
    mock_current_version.return_value = semantic_version.Version("0.1.1")
    mock_recommended_version = mocker.patch.object(AutoUpgrade, "get_recommended_version")
    mock_recommended_version.return_value = semantic_version.Version("0.1.2")
    mock_restart = mocker.patch.object(AutoUpgrade, "restart")
    result = testdir.runpytest(*[
        "--verbose",
        "-p",
        "python_agent.test_listener.integrations.pytest_helper",
        "-p",
        "no:sealights-python-agent",
        "--customer_id=%s" % agent_params["customer_id"],
        "--app_name=%s" % agent_params["app_name"],
        "--server=%s" % agent_params["server"]
    ])
    assert mocks["mock_upgrade_install"].called
    assert mock_restart.called
    result.assert_outcomes(passed=2)


def test_autoupgrade_lower_version(testdir, agent_params, mocker, mocks):
    testdir.makepyfile(
        """
        def test_3plus3():
            assert 3+3 == 6

        def test_1plus1():
            assert 1+1 == 2
        """
    )
    mocks["mock_upgrade_install"].return_value = 0
    mock_current_version = mocker.patch.object(AutoUpgrade, "get_current_version")
    mock_current_version.return_value = semantic_version.Version("0.1.2")
    mock_recommended_version = mocker.patch.object(AutoUpgrade, "get_recommended_version")
    mock_recommended_version.return_value = semantic_version.Version("0.0.1")
    mock_restart = mocker.patch.object(AutoUpgrade, "restart")
    result = testdir.runpytest(*[
        "--verbose",
        "-p",
        "python_agent.test_listener.integrations.pytest_helper",
        "-p",
        "no:sealights-python-agent",
        "--customer_id=%s" % agent_params["customer_id"],
        "--app_name=%s" % agent_params["app_name"],
        "--server=%s" % agent_params["server"]
    ])
    assert mocks["mock_upgrade_install"].called
    assert mock_restart.called
    result.assert_outcomes(passed=2)
