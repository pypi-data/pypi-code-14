from adaptivepy.util.observer_pattern import Observable


class Monitor:
    """
    Interface for a monitor which specifies a mean to acquire the value of a
    contextual parameter.

    It is assumed immutable in term of its possible values.
    """

    def value(self):
        """
        :return: Value of the monitored parameter
        """
        raise NotImplementedError()

    def possible_values(self):
        """
        :return: All possibilities which can be returned by #value
        :rtype: set[obj]
        """
        raise NotImplementedError()


class DynamicMonitor(Monitor, Observable):
    """
    Interface for a monitor which allows to notify registered observers of an
    update to the monitored value
    """

    def start(self):
        """
        Start monitoring the parameter value for changes
        """
        raise NotImplementedError()

    def stop(self):
        """
        Stop monitoring the parameter value for changes
        """
        raise NotImplementedError()

    def is_started(self):
        """
        :return: True if the monitor is started, False otherwise
        :rtype: bool
        """
        raise NotImplementedError()

    def latest_value(self):
        """
        :return: Latest value provided by the monitor
        """
        raise NotImplementedError()

    def _set_latest_value(self, value):
        """
        Allows to set the latest value
        """
        raise NotImplementedError()

    def update(self):
        """
        Update the monitor by checking for a new value and if it is considered
        as a new value.
        """
        latest_value = self.latest_value()
        value = self.value()
        if value != latest_value:
            self._set_latest_value(value)  # Latest value = value before
            # notifying
            self.notify(value, old_value=latest_value)

    def swap(self, other):
        """
        :type other: DynamicMonitor
        """
        Observable.swap(self, other)
        if other.is_started() != self.is_started():
            to_start, to_stop = (self, other) if other.is_started() else \
                                (other, self)
            to_start.start()
            to_stop.stop()

    def register(self, observer):
        super().register(observer)
        if not self.is_started():
            self.start()

    def unregister(self, observer):
        super().unregister(observer)
        if not self._observers and self.is_started():
            self.stop()


class DynamicMonitorDecorator(DynamicMonitor):
    """
    Abstract class for a dynamic monitor used as a decorator over an existing
    static monitor.

    Any derived class which doesn't modify the get value has the property to
    act in a stateless way if the dynamic monitor has not been started
    """

    def __init__(self, monitor_delegate):
        """
        :param monitor_delegate: Monitor to delegate the data acquisition
        :type monitor_delegate: Monitor
        """
        super().__init__()
        self._started = False
        self._latest_value = None
        self._delegate = monitor_delegate

    def value(self):
        return self._delegate.value()

    def possible_values(self):
        return self._delegate.possible_values()

    def start(self):
        if not self.is_started():
            self._started = True
            self.update()

    def stop(self):
        self._started = False

    def is_started(self):
        return self._started

    def latest_value(self):
        return self._latest_value

    def _set_latest_value(self, value):
        self._latest_value = value
