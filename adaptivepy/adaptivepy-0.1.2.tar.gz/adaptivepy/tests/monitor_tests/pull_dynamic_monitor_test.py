import unittest
from unittest.mock import Mock

from adaptivepy.monitor.primitives import Monitor
from adaptivepy.monitor.pull_dynamic_monitor import PullDynamicMonitorDecorator
from adaptivepy.util.observer_pattern import Observer

from adaptivepy.monitor.parameter import DiscreteParameter


class SomeDiscreteParameter(DiscreteParameter):
    s_state0 = 0
    s_state1 = 1
    s_state2 = 2


class PullDynamicMonitorTestCase(unittest.TestCase):
    def setUp(self):
        self.monitor_mock = Mock(Monitor)
        self.monitor_mock.value.return_value = SomeDiscreteParameter.s_state0
        self.monitor_mock.possible_values.return_value = \
            SomeDiscreteParameter.possible_values()
        self.pull_monitor = PullDynamicMonitorDecorator(self.monitor_mock)

    def test_possible_values(self):
        self.assertEqual(self.pull_monitor.possible_values(),
                         SomeDiscreteParameter.possible_values())

    def test_value(self):
        # Not started
        self.assertEqual(self.pull_monitor.value(), None)
        self.assertEqual(self.pull_monitor.latest_value(), None)

        # Start
        self.pull_monitor.start()
        value = self.pull_monitor.value()
        self.assertEqual(value, self.pull_monitor.latest_value())
        self.assertIn(value, self.pull_monitor.possible_values())

        # Stop
        self.pull_monitor.stop()
        self.assertEqual(value, self.pull_monitor.value())
        self.assertEqual(value, self.pull_monitor.latest_value())

    def test_update(self):
        def assert_value_and_latest(value, latest_value):
            self.assertEqual(value, self.pull_monitor.value())
            self.assertEqual(latest_value, self.pull_monitor.latest_value())
            self.assertEqual(latest_value, value)

        self.pull_monitor.start()
        pre_value = self.pull_monitor.value()
        pre_latest_value = self.pull_monitor.latest_value()
        self.monitor_mock.value.return_value = SomeDiscreteParameter.s_state2
        assert_value_and_latest(pre_value, pre_latest_value)

        self.pull_monitor.update()
        post_value = self.pull_monitor.value()
        post_latest_value = self.pull_monitor.latest_value()
        self.assertEqual(post_value, SomeDiscreteParameter.s_state2)
        assert_value_and_latest(post_value, post_latest_value)

    def test_register(self):
        observer_mock = Mock(Observer)
        self.assertEqual(0, self.pull_monitor.registered_count())
        self.pull_monitor.register(observer_mock)
        self.assertEqual(1, self.pull_monitor.registered_count())

        self.monitor_mock.value.return_value = SomeDiscreteParameter.s_state2
        self.pull_monitor.update()

        self.assertTrue(observer_mock.observed_update.called)
        self.assertTrue(observer_mock.observed_update.called_with(
            SomeDiscreteParameter,
            SomeDiscreteParameter.s_state0,
            SomeDiscreteParameter.s_state2
        ))


if __name__ == '__main__':
    unittest.main()
