import unittest
from unittest.mock import Mock

from adaptivepy.monitor.monitor_event_manager import MonitorEventManager
from adaptivepy.monitor.parameter_event import \
    MonitorAlreadyRegisteredException, ImproperMonitorForParameterException, \
    ParameterValueSubscriber
from adaptivepy.monitor.primitives import Monitor
from adaptivepy.monitor.pull_dynamic_monitor import PullDynamicMonitorDecorator

from adaptivepy.monitor.parameter import DiscreteParameter


class SomeDiscreteParameter(DiscreteParameter):
    s_state0 = 0
    s_state1 = 1
    s_state2 = 2


class OtherDiscreteParameter(DiscreteParameter):
    o_state0 = 0
    o_state1 = 1


class MutableMonitor(Monitor):
    def __init__(self, parameter):
        self.__parameter = parameter
        self.__value = parameter(0)

    def possible_values(self):
        return self.__parameter.possible_values()

    def value(self):
        return self.__value

    def set_value(self, state):
        assert state in self.possible_values()
        self.__value = state


class MonitorEventManagerTestCase(unittest.TestCase):
    def setUp(self):
        self.mnt_evt_mng = MonitorEventManager()
        self.static_monitor = MutableMonitor(SomeDiscreteParameter)
        self.pull_decorator = PullDynamicMonitorDecorator(self.static_monitor)

    def change_state(self, state):
        self.static_monitor.set_value(state)
        self.pull_decorator.update()

    def test_register_monitor(self):
        with self.assertRaises(ValueError):
            self.mnt_evt_mng.register_monitor(SomeDiscreteParameter,
                                              self.static_monitor)
        with self.assertRaises(ImproperMonitorForParameterException):
            self.mnt_evt_mng.register_monitor(OtherDiscreteParameter,
                                              self.pull_decorator)

        self.mnt_evt_mng.register_monitor(SomeDiscreteParameter,
                                          self.pull_decorator)

        registered_monitor = self.mnt_evt_mng._param_monitors.get_value(
            SomeDiscreteParameter)
        self.assertIs(registered_monitor, self.pull_decorator)

        with self.assertRaises(MonitorAlreadyRegisteredException):
            self.mnt_evt_mng.register_monitor(SomeDiscreteParameter,
                                              self.pull_decorator)

        unreg_mnt = self.mnt_evt_mng.unregister_monitor(SomeDiscreteParameter)
        self.assertEqual(self.pull_decorator, unreg_mnt)

    def test_subscribe(self):
        param_val_sub_mock = Mock(ParameterValueSubscriber)
        self.mnt_evt_mng.subscribe(param_val_sub_mock, SomeDiscreteParameter)

        self.mnt_evt_mng.register_monitor(SomeDiscreteParameter,
                                          self.pull_decorator)
        self.assertFalse(param_val_sub_mock.updated_monitored_value.called)
        self.change_state(SomeDiscreteParameter.s_state2)
        self.assertTrue(param_val_sub_mock.updated_monitored_value.called)

        try:
            self.mnt_evt_mng.unsubscribe(param_val_sub_mock,
                                         OtherDiscreteParameter)
        except Exception:
            raise AssertionError(
                "Unsubscribing from a parameter not previously subscribed "
                "to should not raise an exception.")

        self.mnt_evt_mng.unsubscribe(param_val_sub_mock, SomeDiscreteParameter)
        param_val_sub_mock.reset_mock()
        self.change_state(SomeDiscreteParameter.s_state1)
        self.assertFalse(param_val_sub_mock.updated_monitored_value.called)

    def test_snapshot(self):
        self.assertFalse(self.mnt_evt_mng.snapshot())
        self.assertIsNone(self.mnt_evt_mng.snapshot({SomeDiscreteParameter})
                          [SomeDiscreteParameter])

        self.mnt_evt_mng.register_monitor(SomeDiscreteParameter,
                                          self.pull_decorator)

        # Not started, ensures there's a valid value (within parameter's
        # possible values)
        snapshot = self.mnt_evt_mng.snapshot({SomeDiscreteParameter})
        not_started_value = snapshot[SomeDiscreteParameter]
        self.assertIs(not_started_value, SomeDiscreteParameter.s_state0)

        self.change_state(SomeDiscreteParameter.s_state2)
        snapshot = self.mnt_evt_mng.snapshot({SomeDiscreteParameter})
        started_value = snapshot[SomeDiscreteParameter]
        self.assertEqual(started_value, SomeDiscreteParameter.s_state2)

        other_pull_monitor = PullDynamicMonitorDecorator(
            MutableMonitor(OtherDiscreteParameter))
        self.mnt_evt_mng.register_monitor(OtherDiscreteParameter,
                                          other_pull_monitor)
        snapshot = self.mnt_evt_mng.snapshot()
        filtered_snapshot = self.mnt_evt_mng.snapshot({SomeDiscreteParameter,
                                                       OtherDiscreteParameter})
        expected_snapshot = {
            SomeDiscreteParameter: SomeDiscreteParameter.s_state2,
            OtherDiscreteParameter: OtherDiscreteParameter.o_state0
        }

        self.assertEqual(snapshot, expected_snapshot)
        self.assertEqual(filtered_snapshot, expected_snapshot)
        snapshot = self.mnt_evt_mng.snapshot({OtherDiscreteParameter})
        self.assertEqual(snapshot, {
            OtherDiscreteParameter: OtherDiscreteParameter.o_state0
        })


if __name__ == '__main__':
    unittest.main()
