class Observer:
    """
    Observer based on the observer pattern
    """
    def observed_update(self, observable, value, **kwarg):
        raise NotImplementedError()


class Observable:
    """
    Observable based on the observer pattern
    """
    def __init__(self):
        super().__init__()
        self._observers = set()

    def register(self, observer):
        assert(isinstance(observer, Observer))
        self._observers.add(observer)

    def unregister(self, observer):
        self._observers.remove(observer)

    def notify(self, value, **kwargs):
        for o in self._observers:
            o.observed_update(self, value, **kwargs)

    def registered_count(self):
        return len(self._observers)

    def swap(self, other):
        """
        :type other: Observable
        """
        self._observers, other._observers = other._observers, self._observers
