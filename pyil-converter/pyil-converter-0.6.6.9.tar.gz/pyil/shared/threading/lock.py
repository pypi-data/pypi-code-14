import time as _time
class LockVar:
    def __init__(self, obj, default_state=None, block_access: bool = True):
        """Create a variable with a lock, will raise
        assertion error when trying to modify the
        value when locked."""
        self._obj = obj
        self._locked = default_state
        self._blocked = block_access

    @property
    def locked(self):
        """Returns weather the variable is locked."""
        return self._locked

    @property
    def value(self):
        """Returns the value of this obj. Will wait
        until the variable is unlocked if block_access
        if set to True."""
        if self._blocked:
            while True:
                if not self._locked:
                    return self._obj
        return self._obj

    def modify(self, new_value):
        """Modify the value."""
        assert self._locked is False, "Can't modify a variable while it is locked."
        self._obj = new_value
        return self.value

    def lock(self, interval: int = 0):
        """Wait until the object is unlocked, then lock it.
        interval is the time to sleep between each check."""
        while True:
            _time.sleep(interval)
            if not self._locked:
                self._locked = True
                break

    def unlock(self):
        """Unlock the variable."""
        assert self._locked is True, 'Variable already unlocked.'
        self._locked = True
