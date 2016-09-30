from adaptivepy.monitor.parameter_event import ParameterValueProvider,\
    MonitorAlreadyRegisteredException, ImproperMonitorForParameterException
from adaptivepy.monitor.primitives import DynamicMonitor

from adaptivepy.util.double_indexed_dictionary import DoubleIndexedDictionary
from adaptivepy.util.observer_pattern import Observer


class MonitorEventManager(Observer, ParameterValueProvider):
    """
    Manager for all monitors of a session
    """

    def __init__(self):
        super().__init__()
        self._param_monitors = DoubleIndexedDictionary()
        self._snapshot = {}  # Snapshot of the manager over local context
        self._subscribers = {}
        """:type: dict[Parameter, set[ParameterValueSubscriber]]"""

    def snapshot(self, parameters=None):
        return self._snapshot if not parameters else \
            {p: self._snapshot.get(p, None) for p in parameters}

    def observed_update(self, observable, value, **kwarg):
        parameter = self._param_monitors.get_key(observable)
        self._snapshot[parameter] = value

        subscribers = self._subscribers.get(parameter, set()).copy()
        for s in subscribers:
            try:
                s.updated_monitored_value(parameter, kwarg["old_value"], value)
            except RuntimeError as e:
                # If a runtime error is raised while updating, but hasn't been
                # catched by the client, unsubscribe it to prevent further
                # problems and allow other subscribers to receive the values
                print(e)
                self.unsubscribe(s, parameter)

    def subscribe(self, subscriber, parameter):
        """
        :param subscriber:
        :param parameter:
        :return:
        """
        if parameter not in self._subscribers:
            self._subscribers[parameter] = set()
        self._subscribers[parameter].add(subscriber)

    def unsubscribe(self, subscriber, parameter):
        if parameter in self._subscribers:
            subscribers = self._subscribers[parameter]
            if subscriber in subscribers:
                subscribers.remove(subscriber)

    def register_monitor(self, parameter, monitor):
        """
        :param parameter: Adaptation parameter
        :type parameter: Parameter
        :type monitor: DynamicMonitor
        :raises: ValueError | ImproperMonitorForParameterException |
                 MonitorAlreadyRegisteredException
        """
        if not isinstance(monitor, DynamicMonitor):
            raise ValueError(
                "The provided monitor must be dynamic (see DynamicMonitor)")

        if not monitor.possible_values().issubset(parameter.possible_values()):
            raise ImproperMonitorForParameterException(
                "The monitor's possible values must be a subset of the "
                "parameter's.\n",
                parameter,
                monitor
            )

        if self._param_monitors.is_key_in(parameter):
            raise MonitorAlreadyRegisteredException(
                "Parameter '{}' is already monitored by '{}'".format(
                    parameter, self._param_monitors.get_value(parameter)
                ))

        self._param_monitors.add(parameter, monitor)
        if monitor.latest_value() is None:
            monitor.update()  # Ensure a value
        self._snapshot[parameter] = monitor.latest_value()

        # TODO: Register only if subscriber to the parameter exist
        monitor.register(self)  # Register to further updates

    def unregister_monitor(self, parameter):
        monitor = self._param_monitors.pop(parameter)
        if monitor:
            monitor.unregister(self)
        return monitor

    def replace_monitor(self, parameter, new_monitor):
        """
        :type parameter: Parameter
        :type new_monitor: DynamicMonitor
        """
        self.unregister_monitor(parameter)
        self.register_monitor(parameter, new_monitor)

    def __str__(self):
        return "Monitored parameters: " + str(self._param_monitors)


GLOBAL_MONITORS_EVENT_MANAGER = MonitorEventManager()


def register_global_monitor(parameter, monitor):
    GLOBAL_MONITORS_EVENT_MANAGER.register_monitor(parameter, monitor)
