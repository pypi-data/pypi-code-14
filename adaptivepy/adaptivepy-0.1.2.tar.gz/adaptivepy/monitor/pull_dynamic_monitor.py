from adaptivepy.monitor.primitives import DynamicMonitorDecorator


class PullDynamicMonitorDecorator(DynamicMonitorDecorator):
    """
    Decorator that requests a value when starting and always provides
    the same thereafter until a manual update is request or it is restarted.
    """

    def __init__(self, monitor_delegate):
        super().__init__(DynamicMonitorDecorator(monitor_delegate))
        self._delegate.notify = self.notify
        self._delegate.start = self.start
        self._delegate.stop = self.stop
        self._delegate.is_started = self.is_started

    def value(self):
        return self._delegate.latest_value()

    def latest_value(self):
        return self._delegate.latest_value()

    def update(self):
        self._delegate.update()
