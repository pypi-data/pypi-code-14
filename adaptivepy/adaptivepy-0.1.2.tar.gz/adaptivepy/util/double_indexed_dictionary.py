from threading import Lock


class DoubleIndexedDictionary:
    """
    Dictionary-like class which indexes the pairs both in term of key and value.
    """
    def __init__(self):
        self._lock = Lock()
        self._base_dict = {}
        self._inverse_dict = {}

        self.get = self.get_value
        self.pop = self.pop_value

    def add(self, key, value):
        self._lock.acquire()
        self._base_dict[key] = value
        self._inverse_dict[value] = key
        self._lock.release()

    def _pop_from(self, first, second, item):
        self._lock.acquire()
        try:
            value = first.pop(item)
            second.pop(value)
        finally:
            self._lock.release()
        return value

    def pop_value(self, key):
        return self._pop_from(self._base_dict, self._inverse_dict, key)

    def pop_key(self, value):
        return self._pop_from(self._inverse_dict, self._base_dict, value)

    def get_value(self, key):
        return self._base_dict.get(key)

    def get_key(self, value):
        return self._inverse_dict.get(value)

    def is_key_in(self, key):
        return key in self._base_dict

    def is_value_in(self, value):
        return value in self._inverse_dict

    def keys(self):
        return self._base_dict.keys()

    def values(self):
        return self._base_dict.values()

    def items(self):
        return self._base_dict.items()

    def clear(self):
        self._lock.acquire()
        self._base_dict.clear()
        self._inverse_dict.clear()
        self._lock.release()

    def __contains__(self, item):
        return self.is_key_in(item)

    def __getitem__(self, item):
        return self.get_value(item)

    def __setitem__(self, key, value):
        self.add(key, value)

    def __len__(self):
        return len(self._base_dict)

    def __str__(self):
        return str(self._base_dict)
