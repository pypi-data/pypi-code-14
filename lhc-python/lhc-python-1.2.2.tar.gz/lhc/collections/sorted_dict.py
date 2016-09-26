from bisect import bisect_left


class SortedDict(object):
    def __init__(self, iterable=None):
        """Create a sorted dictionary
        
        :param iterable: the initial key:value pairs to put in the dictionary
        :type iterable: list of tuple
        """
        if iterable is None:
            self._keys = []
            self._values = []
        else:
            self._keys, self._values = [list(r) for r in zip(*sorted(iterable))]
    
    def __str__(self):
        return '{%s}' % ', '.join(['%s:%s' % entry for entry in self.items()])
    
    def __iter__(self):
        return iter(self._keys)
    
    def __len__(self):
        return len(self._keys)
    
    def __contains__(self, key):
        idx = bisect_left(self._keys, key)
        return idx < len(self._keys) and self._keys[idx] == key
    
    def __getitem__(self, key):
        idx = bisect_left(self._keys, key)
        if idx == len(self._keys) or self._keys[idx] != key:
            raise KeyError(key)
        return self._values[idx]

    def __setitem__(self, key, value):
        idx = bisect_left(self._keys, key)
        if idx >= len(self._keys) or self._keys[idx] != key:
            self._keys.insert(idx, key)
            self._values.insert(idx, value)
        else:
            self._values[idx] = value

    def __delitem__(self, key):
        idx = bisect_left(self._keys, key)
        del self._keys[idx]
        del self._values[idx]
    
    def get(self, key, default):
        try:
            return self[key]
        except KeyError:
            pass
        return default
    
    def keys(self):
        return iter(self._keys)
    
    def values(self):
        return iter(self._values)
    
    def items(self):
        return list(zip(self._keys, self._values))

    def pop_highest(self):
        key = self._keys.pop()
        value = self._values.pop()
        return key, value

    def pop_lowest(self):
        key = self._keys.pop(0)
        value = self._values.pop(0)
        return key, value
