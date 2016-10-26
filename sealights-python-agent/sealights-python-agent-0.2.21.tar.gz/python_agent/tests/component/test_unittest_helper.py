import os
import unittest
import unittest2


from mock import patch, ANY

from python_agent.admin import cli
from python_agent.packages.click.testing import CliRunner
from python_agent import config
from python_agent.test_listener.agent_manager import AgentManager
from python_agent.test_listener.sealights_api import SeaLightsAPI
from python_agent.test_listener.state_tracker import StateTracker
from python_agent.test_listener.utils import Singleton
from python_agent.tests.component.data.unittest_helper import SanityTestCase, PassSkipTestCase, AllSkipTestCase, \
    PassErrorTestCase
from python_agent.utils.autoupgrade import AutoUpgrade

config.INTERVAL_IN_MILLISECONDS = 50
data_file_path = os.path.abspath(__file__)
agent_params = {
    "customer_id": "customer",
    "app_name": "agent",
    "server": "http://someserver/api"
}


class OrchestratorTestCase(unittest.TestCase):

    def setUp(self):
        Singleton._instances.pop(AgentManager)
        Singleton._instances.pop(StateTracker)

    @patch("python_agent.utils.autoupgrade.AutoUpgrade.install")
    @patch("pkg_resources.get_distribution", spec=True)
    @patch("python_agent.packages.requests.get", spec=True)
    @patch("python_agent.packages.requests.post", spec=True)
    def test_sanity(self, mock_post, mock_get, mock_get_distribution, mock_upgrade_install):
        mock_get_distribution.return_value.version = "0.1.1"
        event_types = ['executionIdStarted', 'testStart', 'testEnd', 'testStart', 'testEnd', 'executionIdEnded']
        runner = CliRunner()
        result = runner.invoke(cli, [
            "--customer_id", agent_params["customer_id"],
            "--app_name", agent_params["app_name"],
            "--server", agent_params["server"],
            "--source", data_file_path,
            "unittest",
            "-vv",
            SanityTestCase.__module__ + "." + SanityTestCase.__name__
        ])
        assert result.exit_code == 0
        all_events = []
        for (args, kwargs) in mock_post.call_args_list:
            if args[0] != agent_params["server"] + config.TEST_EVENTS_ROUTE:
                continue
            message = kwargs.get("json", {})
            assert message.get("customerId", "") == agent_params["customer_id"]
            assert message.get("appName", "") == agent_params["app_name"]
            assert message.get("branch", "") == "master"
            assert message.get("build", "") == "1"
            events = message.get("events", [])
            assert events
            all_events.extend(events)
        assert len(all_events) == 6
        for event in all_events:
            if event.get("type") == "testEnd":
                assert event.get("result") == "passed"
        assert sorted(map(lambda event: event.get("type"), all_events)) == sorted(event_types)

    @patch("python_agent.utils.autoupgrade.AutoUpgrade.install")
    @patch("pkg_resources.get_distribution", spec=True)
    @patch("python_agent.packages.requests.get", spec=True)
    @patch("python_agent.packages.requests.post", spec=True)
    def test_pass_skip(self, mock_post, mock_get, mock_get_distribution, mock_upgrade_install):
        mock_get_distribution.return_value.version = "0.1.1"
        runner = CliRunner()
        result = runner.invoke(cli, [
            "--customer_id", agent_params["customer_id"],
            "--app_name", agent_params["app_name"],
            "--server", agent_params["server"],
            "--source", data_file_path,
            "unittest",
            "-vv",
            PassSkipTestCase.__module__ + "." + PassSkipTestCase.__name__
        ])
        assert result.exit_code == 0

        all_events = []
        for index, (args, kwargs) in enumerate(mock_post.call_args_list):
            if args[0] != agent_params["server"] + config.TEST_EVENTS_ROUTE:
                continue
            message = kwargs.get("json", {})
            events = message.get("events", [])
            assert events
            all_events.extend(events)
        assert len(all_events) == 6
        for event in all_events:
            if "test_3plus3" in event.get("testName", "") and event.get("type") == "testEnd":
                assert event.get("result") == "passed"
            if "test_1plus1" in event.get("testName", "") and event.get("type") == "testEnd":
                assert event.get("result") == "skipped"

    @patch("python_agent.utils.autoupgrade.AutoUpgrade.install")
    @patch("pkg_resources.get_distribution", spec=True)
    @patch("python_agent.packages.requests.get", spec=True)
    @patch("python_agent.packages.requests.post", spec=True)
    def test_all_skip(self, mock_post, mock_get, mock_get_distribution, mock_upgrade_install):
        mock_get_distribution.return_value.version = "0.1.1"
        runner = CliRunner()
        result = runner.invoke(cli, [
            "--customer_id", agent_params["customer_id"],
            "--app_name", agent_params["app_name"],
            "--server", agent_params["server"],
            "--source", data_file_path,
            "unittest",
            "-vv",
            AllSkipTestCase.__module__ + "." + AllSkipTestCase.__name__
        ])
        assert result.exit_code == 0

        all_events = []
        for (args, kwargs) in mock_post.call_args_list:
            if args[0] != agent_params["server"] + config.TEST_EVENTS_ROUTE:
                continue
            message = kwargs.get("json", {})
            events = message.get("events", [])
            assert events
            all_events.extend(events)
        assert len(all_events) == 6
        for event in all_events:
            if event.get("type") == "testEnd":
                assert event.get("result") == "skipped"

    @patch("python_agent.utils.autoupgrade.AutoUpgrade.install")
    @patch("pkg_resources.get_distribution", spec=True)
    @patch("python_agent.packages.requests.get", spec=True)
    @patch("python_agent.packages.requests.post", spec=True)
    def test_pass_error(self, mock_post, mock_get, mock_get_distribution, mock_upgrade_install):
        mock_get_distribution.return_value.version = "0.1.1"
        with patch("unittest.TestCase.assertEqual", spec=True) as mock_assert_equal:
            mock_assert_equal.side_effect = Exception()
            runner = CliRunner()
            result = runner.invoke(cli, [
                "--customer_id", agent_params["customer_id"],
                "--app_name", agent_params["app_name"],
                "--server", agent_params["server"],
                "--source", data_file_path,
                "unittest",
                "-vv",
                PassErrorTestCase.__module__ + "." + PassErrorTestCase.__name__
            ])
            assert result.exit_code == 0

        all_events = []
        for (args, kwargs) in mock_post.call_args_list:
            if args[0] != agent_params["server"] + config.TEST_EVENTS_ROUTE:
                continue
            message = kwargs.get("json", {})
            events = message.get("events", [])
            assert events
            all_events.extend(events)
        assert len(all_events) == 6
        for event in all_events:
            if "test_3plus3" in event.get("testName", "") and event.get("type") == "testEnd":
                assert event.get("result") == "passed"
            if "test_1plus1" in event.get("testName", "") and event.get("type") == "testEnd":
                assert event.get("result") == "failed"

    @patch("python_agent.utils.autoupgrade.AutoUpgrade.install")
    @patch("pkg_resources.get_distribution", spec=True)
    @patch("python_agent.packages.requests.get", spec=True)
    @patch("python_agent.packages.requests.post", spec=True)
    def test_pass_failure(self, mock_post, mock_get, mock_get_distribution, mock_upgrade_install):
        mock_get_distribution.return_value.version = "0.1.1"
        with patch("unittest.TestCase.assertEqual", spec=True) as mock_assert_equal:
            mock_assert_equal.side_effect = AssertionError
            runner = CliRunner()
            result = runner.invoke(cli, [
                "--customer_id", agent_params["customer_id"],
                "--app_name", agent_params["app_name"],
                "--server", agent_params["server"],
                "--source", data_file_path,
                "unittest",
                "-vv",
                PassErrorTestCase.__module__ + "." + PassErrorTestCase.__name__
            ])
            assert result.exit_code == 0

        all_events = []
        for (args, kwargs) in mock_post.call_args_list:
            if args[0] != agent_params["server"] + config.TEST_EVENTS_ROUTE:
                continue
            message = kwargs.get("json", {})
            events = message.get("events", [])
            assert events
            all_events.extend(events)
        assert len(all_events) == 6
        for event in all_events:
            if "test_3plus3" in event.get("testName", "") and event.get("type") == "testEnd":
                assert event.get("result") == "passed"
            if "test_1plus1" in event.get("testName", "") and event.get("type") == "testEnd":
                assert event.get("result") == "failed"

    @patch("python_agent.utils.autoupgrade.AutoUpgrade.install")
    @patch("pkg_resources.get_distribution", spec=True)
    @patch.object(SeaLightsAPI, "notify_execution_start")
    @patch("python_agent.packages.requests.get", spec=True)
    @patch("python_agent.packages.requests.post", spec=True)
    def test_execution_start_fail(self, mock_post, mock_get, mock_start, mock_get_distribution, mock_upgrade_install):
        event_types = ['testStart', 'testEnd', 'testStart', 'testEnd', 'executionIdEnded']
        mock_get_distribution.return_value.version = "0.1.1"
        mock_start.side_effect = Exception()
        runner = CliRunner()
        result = runner.invoke(cli, [
            "--customer_id", agent_params["customer_id"],
            "--app_name", agent_params["app_name"],
            "--server", agent_params["server"],
            "--source", data_file_path,
            "unittest",
            "-vv",
            SanityTestCase.__module__ + "." + SanityTestCase.__name__
        ])
        assert result.exit_code == 0

        all_events = []
        for (args, kwargs) in mock_post.call_args_list:
            if args[0] != agent_params["server"] + config.TEST_EVENTS_ROUTE:
                continue
            message = kwargs.get("json", {})
            events = message.get("events", [])
            assert events
            all_events.extend(events)
        assert len(all_events) == 5
        assert sorted(map(lambda event: event.get("type"), all_events)) == sorted(event_types)

    @patch("python_agent.utils.autoupgrade.AutoUpgrade.install")
    @patch("pkg_resources.get_distribution", spec=True)
    @patch.object(SeaLightsAPI, "notify_execution_end")
    @patch("python_agent.packages.requests.get", spec=True)
    @patch("python_agent.packages.requests.post", spec=True)
    def test_execution_end_fail(self, mock_post, mock_get, mock_stop, mock_get_distribution, mock_upgrade_install):
        event_types = ['executionIdStarted', 'testStart', 'testEnd', 'testStart', 'testEnd']
        mock_get_distribution.return_value.version = "0.1.1"
        mock_stop.side_effect = Exception()
        runner = CliRunner()
        result = runner.invoke(cli, [
            "--customer_id", agent_params["customer_id"],
            "--app_name", agent_params["app_name"],
            "--server", agent_params["server"],
            "--source", data_file_path,
            "unittest",
            "-vv",
            SanityTestCase.__module__ + "." + SanityTestCase.__name__
        ])
        assert result.exit_code == 0

        all_events = []
        for (args, kwargs) in mock_post.call_args_list:
            if args[0] != agent_params["server"] + config.TEST_EVENTS_ROUTE:
                continue
            message = kwargs.get("json", {})
            events = message.get("events", [])
            assert events
            all_events.extend(events)
        assert len(all_events) == 5
        assert sorted(map(lambda event: event.get("type"), all_events)) == sorted(event_types)

    @patch("python_agent.utils.autoupgrade.AutoUpgrade.install")
    @patch("pkg_resources.get_distribution", spec=True)
    @patch.object(SeaLightsAPI, "notify_test_start")
    @patch("python_agent.packages.requests.get", spec=True)
    @patch("python_agent.packages.requests.post", spec=True)
    def test_test_start_fail(self, mock_post, mock_get, mock_start_test, mock_get_distribution, mock_upgrade_install):
        event_types = ['executionIdStarted', 'testEnd', 'testEnd', 'executionIdEnded']
        mock_get_distribution.return_value.version = "0.1.1"
        mock_start_test.side_effect = Exception()
        runner = CliRunner()
        result = runner.invoke(cli, [
            "--customer_id", agent_params["customer_id"],
            "--app_name", agent_params["app_name"],
            "--server", agent_params["server"],
            "--source", data_file_path,
            "unittest",
            "-vv",
            SanityTestCase.__module__ + "." + SanityTestCase.__name__
        ])
        assert result.exit_code == 0

        all_events = []
        for (args, kwargs) in mock_post.call_args_list:
            if args[0] != agent_params["server"] + config.TEST_EVENTS_ROUTE:
                continue
            message = kwargs.get("json", {})
            events = message.get("events", [])
            assert events
            all_events.extend(events)
        assert len(all_events) == 4
        assert sorted(map(lambda event: event.get("type"), all_events)) == sorted(event_types)

    @patch("python_agent.utils.autoupgrade.AutoUpgrade.install")
    @patch("pkg_resources.get_distribution", spec=True)
    @patch.object(SeaLightsAPI, "notify_test_end")
    @patch("python_agent.packages.requests.get", spec=True)
    @patch("python_agent.packages.requests.post", spec=True)
    def test_passed_test_fail(self, mock_post, mock_get, mock_passed_test, mock_get_distribution, mock_upgrade_install):
        event_types = ['executionIdStarted', 'testStart', 'testStart', 'executionIdEnded']
        mock_get_distribution.return_value.version = "0.1.1"
        mock_passed_test.side_effect = Exception()
        runner = CliRunner()
        result = runner.invoke(cli, [
            "--customer_id", agent_params["customer_id"],
            "--app_name", agent_params["app_name"],
            "--server", agent_params["server"],
            "--source", data_file_path,
            "unittest",
            "-vv",
            SanityTestCase.__module__ + "." + SanityTestCase.__name__
        ])
        assert result.exit_code == 0

        all_events = []
        for (args, kwargs) in mock_post.call_args_list:
            if args[0] != agent_params["server"] + config.TEST_EVENTS_ROUTE:
                continue
            message = kwargs.get("json", {})
            events = message.get("events", [])
            assert events
            all_events.extend(events)
        assert len(all_events) == 4
        assert sorted(map(lambda event: event.get("type"), all_events)) == sorted(event_types)
        mock_passed_test.assert_any_call(ANY, ANY, ANY, "passed")

    @patch("python_agent.utils.autoupgrade.AutoUpgrade.install")
    @patch("pkg_resources.get_distribution", spec=True)
    @patch.object(SeaLightsAPI, "notify_test_end")
    @patch("python_agent.packages.requests.get", spec=True)
    @patch("python_agent.packages.requests.post", spec=True)
    def test_skipped_test_fail(self, mock_post, mock_get, mock_skipped_test, mock_get_distribution, mock_upgrade_install):
        mock_get_distribution.return_value.version = "0.1.1"
        mock_skipped_test.side_effect = Exception()
        runner = CliRunner()
        result = runner.invoke(cli, [
            "--customer_id", agent_params["customer_id"],
            "--app_name", agent_params["app_name"],
            "--server", agent_params["server"],
            "--source", data_file_path,
            "unittest",
            "-vv",
            PassSkipTestCase.__module__ + "." + PassSkipTestCase.__name__
        ])
        assert result.exit_code == 0

        all_events = []
        for (args, kwargs) in mock_post.call_args_list:
            if args[0] != agent_params["server"] + config.TEST_EVENTS_ROUTE:
                continue
            message = kwargs.get("json", {})
            events = message.get("events", [])
            assert events
            all_events.extend(events)
        assert len(all_events) == 4
        mock_skipped_test.assert_any_call(ANY, ANY, ANY, "passed")
        mock_skipped_test.assert_any_call(ANY, ANY, ANY, "skipped")

    @patch("python_agent.utils.autoupgrade.AutoUpgrade.install")
    @patch("pkg_resources.get_distribution", spec=True)
    @patch.object(SeaLightsAPI, "notify_test_end")
    @patch("python_agent.packages.requests.get", spec=True)
    @patch("python_agent.packages.requests.post", spec=True)
    def test_error_test_fail(self, mock_post, mock_get, mock_failed_test, mock_get_distribution, mock_upgrade_install):
        mock_get_distribution.return_value.version = "0.1.1"
        with patch("unittest.TestCase.assertEqual", spec=True) as mock_assert_equal:
            mock_assert_equal.side_effect = Exception()
            mock_failed_test.side_effect = Exception()
            runner = CliRunner()
            result = runner.invoke(cli, [
                "--customer_id", agent_params["customer_id"],
                "--app_name", agent_params["app_name"],
                "--server", agent_params["server"],
                "--source", data_file_path,
                "unittest",
                "-vv",
                PassErrorTestCase.__module__ + "." + PassErrorTestCase.__name__
            ])
            assert result.exit_code == 0

        all_events = []
        for (args, kwargs) in mock_post.call_args_list:
            if args[0] != agent_params["server"] + config.TEST_EVENTS_ROUTE:
                continue
            message = kwargs.get("json", {})
            events = message.get("events", [])
            assert events
            all_events.extend(events)
        assert len(all_events) == 4
        mock_failed_test.assert_any_call(ANY, ANY, ANY, "passed")
        mock_failed_test.assert_any_call(ANY, ANY, ANY, "failed")

    @patch("python_agent.utils.autoupgrade.AutoUpgrade.install")
    @patch("pkg_resources.get_distribution", spec=True)
    @patch.object(SeaLightsAPI, "notify_test_end")
    @patch("python_agent.packages.requests.get", spec=True)
    @patch("python_agent.packages.requests.post", spec=True)
    def test_fail_test_fail(self, mock_post, mock_get, mock_failed_test, mock_get_distribution, mock_upgrade_install):
        mock_get_distribution.return_value.version = "0.1.1"
        with patch("unittest.TestCase.assertEqual", spec=True) as mock_assert_equal:
            mock_assert_equal.side_effect = AssertionError
            mock_failed_test.side_effect = Exception()
            runner = CliRunner()
            result = runner.invoke(cli, [
                "--customer_id", agent_params["customer_id"],
                "--app_name", agent_params["app_name"],
                "--server", agent_params["server"],
                "--source", data_file_path,
                "unittest",
                "-vv",
                PassErrorTestCase.__module__ + "." + PassErrorTestCase.__name__
            ])
            assert result.exit_code == 0

        all_events = []
        for (args, kwargs) in mock_post.call_args_list:
            if args[0] != agent_params["server"] + config.TEST_EVENTS_ROUTE:
                continue
            message = kwargs.get("json", {})
            events = message.get("events", [])
            assert events
            all_events.extend(events)
        assert len(all_events) == 4
        mock_failed_test.assert_any_call(ANY, ANY, ANY, "passed")
        mock_failed_test.assert_any_call(ANY, ANY, ANY, "failed")

    @patch("python_agent.utils.autoupgrade.AutoUpgrade.install")
    @patch("pkg_resources.get_distribution", spec=True)
    @patch.object(AutoUpgrade, "upgrade", return_value=1)
    @patch("python_agent.packages.requests.Response", spec=True)
    @patch.dict('python_agent.config.app', spec=True, wraps=config.app)
    @patch("python_agent.packages.requests.get", spec=True)
    @patch("python_agent.packages.requests.post", spec=True)
    def test_config_from_server(self, mock_post, mock_get, mock_response, mock_upgrade, mock_get_distribution,
                                mock_upgrade_install):
        mock_get_distribution.return_value.version = "0.1.1"
        mock_response.json.return_value = {
            'meta': {
                'query': 'Python',
                'generated': '2016-08-29T14:33:34.852Z',
                'version': '1.7.265',
                'customerId': 'nutanix'
            },
            'config': '{"featuresData.enableSendLogs":true}'
        }
        mock_get.return_value = mock_response
        runner = CliRunner()
        result = runner.invoke(cli, [
            "--customer_id", agent_params["customer_id"],
            "--app_name", agent_params["app_name"],
            "--server", agent_params["server"],
            "--source", data_file_path,
            "unittest",
            "-vv",
            PassSkipTestCase.__module__ + "." + PassSkipTestCase.__name__
        ])
        assert result.exit_code == 0

        assert config.app.get("featuresData.enableSendLogs")
        assert mock_get.call_count == 1

    @patch("unittest2.TestProgram.__init__", return_value=None)
    @patch("unittest.TestProgram.__init__", return_value=None)
    @patch("python_agent.utils.autoupgrade.AutoUpgrade.install")
    @patch("pkg_resources.get_distribution", spec=True)
    @patch.object(AutoUpgrade, "upgrade", return_value=1)
    @patch("python_agent.packages.requests.Response", spec=True)
    @patch.dict('python_agent.config.app', spec=True, wraps=config.app)
    @patch("python_agent.packages.requests.get", spec=True)
    @patch("python_agent.packages.requests.post", spec=True)
    def test_unittest_vs_unittest2(self, mock_post, mock_get, mock_response, mock_upgrade, mock_get_distribution,
                                   mock_upgrade_install, mock_unittest, mock_unittest2):
        runner = CliRunner()

        runner.invoke(cli, [
            "--customer_id", agent_params["customer_id"],
            "--app_name", agent_params["app_name"],
            "--server", agent_params["server"],
            "--source", ".",
            "unit2",
            "some_test"
        ])

        unittest_helper_module = __import__("python_agent.test_listener.integrations.unittest_helper",
                                            fromlist=["SealightsTestProgram"])
        sl_test_program = getattr(unittest_helper_module, "SealightsTestProgram")
        assert sl_test_program.__bases__[0] == unittest2.TestProgram

        runner.invoke(cli, [
            "--customer_id", agent_params["customer_id"],
            "--app_name", agent_params["app_name"],
            "--server", agent_params["server"],
            "--source", ".",
            "unittest",
            "some_test"
        ])

        unittest_helper_module = __import__("python_agent.test_listener.integrations.unittest_helper",
                                            fromlist=["SealightsTestProgram"])
        sl_test_program = getattr(unittest_helper_module, "SealightsTestProgram")
        assert sl_test_program.__bases__[0] == unittest.TestProgram
