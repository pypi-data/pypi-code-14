from threading import Timer

from adaptivepy.monitor.primitives import DynamicMonitorDecorator


class PollingDynamicMonitorDecorator(DynamicMonitorDecorator):
    """
    Abstract decorator to add dynamic behavior to a monitor through polling
    """

    def __init__(self, monitor_delegate, delay=None):
        """
        :type monitor_delegate: DynamicMonitor
        :param delay: Delay in seconds for polling
        """
        super().__init__(monitor_delegate)
        self._delay = delay or 1.0
        self._create_timer = lambda: Timer(self._delay,
                                           self._timer_update)
        """:type: () -> Timer"""

        self._timer = None
        """:type: Timer"""

    def start(self):
        super().start()
        self._timer = self._create_timer()
        self._timer.start()
        self.update()

    def stop(self):
        super().stop()
        if self._timer:
            self._timer.cancel()

    def _timer_update(self):
        self.start()
        self.update()

    def update(self):
        value = self.value()
        if value != self._latest_value:
            old_value = self._latest_value
            self._latest_value = value  # Latest value = value before notifying
            self.notify(value, old_value=old_value)
