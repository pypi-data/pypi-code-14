from __future__ import absolute_import
import collections
from json import JSONEncoder

try:
    from types import MappingProxyType
except ImportError:
    MappingProxyType = lambda x: x # noop

class FrozenDict(collections.Mapping):
    '''Immutable dictionary.'''

    def __init__(self, *args, **kwargs):
        self._dict = MappingProxyType(dict(*args, **kwargs))
        self._hash = None

    def __getitem__(self, key):
        '''Pass-through to internal dict.'''
        return self._dict[key]

    def __iter__(self):
        '''Pass-through to internal dict.'''
        return iter(self._dict)

    def __len__(self):
        '''Pass-through to internal dict.'''
        return len(self._dict)

    def __hash__(self):
        '''Caches lazily-computed hash value.'''
        if self._hash is None:
            self._hash = hash(frozenset(self._dict.items()))
        return self._hash

    def __repr__(self): # pragma: no cover
        items = ('{}: {}'.format(repr(k),repr(v)) for k,v in sorted(self.items()))
        return '{}({{{}}})'.format(type(self).__name__, ', '.join(items))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self._dict == other._dict

class FrozenDictEncoder(JSONEncoder):
    '''Custom JSON encoder that converts FrozenDict to a dict.'''
    def default(self, obj):
        if isinstance(obj, FrozenDict):
            return dict(obj)
        return JSONEncoder.default(self, obj) # pragma: no cover


