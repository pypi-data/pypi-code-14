__all__ = ['triedict']
from collections import defaultdict, MutableMapping

class AmbiguousKey(KeyError):
    pass

class KeyNotFound(KeyError):
    pass

def _dictdefaultdict():
    return defaultdict(_dictdefaultdict)

def _chars(key):
    for i in range(len(key)):
        yield key[i:i+1]

def _iter_trie_dict(prefix, d):
    for k, v in d.items():
        if k == None:
            yield prefix
        else:
            yield from _iter_trie_dict(prefix + k, v)

class triedict(MutableMapping):
    def __init__(self, *args, **kwargs):
        self._type = None
        self._trie = _dictdefaultdict()
        self.update(dict(*args, **kwargs))

    def _check_type(self, key):
        if self._type:
            if isinstance(key, self._type):
                pass # good
            else:
                raise TypeError('Key must be of %s type.' % self._type)
        else:
            if hasattr(key, '__iter__'):
                self._type = type(key)
            else:
                raise TypeError('Key must be iterable.')

    def __repr__(self):
        return 'triedict(%s)' % repr(dict(self.items()))

    def __getitem__(self, key):
        self._check_type(key)
        d = self._trie
        subkey = [None] + list(key)
        for char in _chars(key):
            if char in d:
                d = d[char]
                subkey = subkey[1:]
            else:
                break

        if None in d:
            if len(subkey) == 1:
                return d[None]
            else:
                raise KeyNotFound('Not found: ' + str(key))
        else:
            while None not in d and len(d) == 1:
                d = d[next(iter(d))]
                subkey = subkey[1:]

            if len(d) > 1:
                if (not subkey) or (subkey[0] in d):
                    raise AmbiguousKey('Ambiguous: ' + str(key))
                else:
                    raise KeyNotFound('Not found: ' + str(key))
            elif len(d) == 0 or None not in d:
                raise KeyNotFound('Not found: ' + str(key))
            else:
                return d[None]

    def __setitem__(self, key, value):
        self._check_type(key)
        d = self._trie
        for char in _chars(key):
            d = d[char]
        d[None] = value

    def __delitem__(self, key):
        self._check_type(key)
        raise NotImplementedError

    def __iter__(self):
        d = self._trie
        if d:
            return _iter_trie_dict(self._type(), d)
        else:
            return iter([])

    def __len__(self):
        n = 0
        for _ in self:
            n += 1
        return n
