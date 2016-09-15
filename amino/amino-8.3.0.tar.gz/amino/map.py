from typing import TypeVar, Dict, Generic, Tuple, Callable

from toolz import dicttoolz

from amino import Maybe, may, Just
from amino.list import List
from amino.boolean import Boolean

A = TypeVar('A')
B = TypeVar('B')
C = TypeVar('C')
D = TypeVar('D')


class Map(Dict[A, B], Generic[A, B]):  # type: ignore

    @staticmethod
    def wrap(d: Dict[A, B]) -> 'Map[A, B]':
        return Map(d)

    @may
    def get(self, key):
        return Dict.get(self, key)

    def get_item(self, key):
        return self.get(key) / (lambda a: (key, a))

    def get_all(self, *keys):
        def append(zm, k):
            return zm // (lambda z: self.get(k) / z.cat)
        return List.wrap(keys).fold_left(Just(List()))(append)

    def get_all_map(self, *keys):
        def append(zm, k):
            return zm // (lambda z: self.get_item(k) / z.cat)
        return List.wrap(keys).fold_left(Just(Map()))(append)

    def get_or_else(self, key, default: Callable[[], C]):
        return self.get(key).get_or_else(default)

    def set_if_missing(self, key: A, default: Callable[[], B]):
        if key in self:
            return self
        else:
            return self + (key, default())

    def __str__(self):
        return str(dict(self))

    def cat(self, item: Tuple[A, B]):
        return Map(dicttoolz.assoc(self, *item))

    __add__ = cat

    def merge(self, other: 'Map[A, B]'):
        return Map(dicttoolz.merge(self, other))

    __pow__ = merge

    def __sub__(self, key: A):
        return Map(dicttoolz.dissoc(self, key))

    def find(self, f: Callable[[B], bool]) -> Maybe[Tuple[A, B]]:
        return self.to_list.find(lambda item: f(item[1]))

    def find_key(self, f: Callable[[A], bool]) -> Maybe[Tuple[A, B]]:
        return self.to_list.find(lambda item: f(item[0]))

    def valfilter(self, f: Callable[[B], bool]) -> 'Map[A, B]':
        return Map(dicttoolz.valfilter(f, self))

    def keyfilter(self, f: Callable[[A], bool]) -> 'Map[A, B]':
        return Map(dicttoolz.keyfilter(f, self))

    def filter(self, f: Callable[[Tuple[A, B]], bool]) -> 'Map[A, B]':
        return Map(dicttoolz.itemfilter(f, self))

    def valmap(self, f: Callable[[B], C]) -> 'Map[A, C]':
        return Map(dicttoolz.valmap(f, dict(self)))

    def keymap(self, f: Callable[[A], C]) -> 'Map[C, B]':
        return Map(dicttoolz.keymap(f, dict(self)))

    def map(self, f: Callable[[Tuple[A, B]], Tuple[C, D]]) -> 'Map[C, D]':
        return Map(dicttoolz.itemmap(f, self))

    def flat_map(
            self,
            f: Callable[[A, B], Maybe[Tuple[C, D]]]
    ) -> 'Map[C, D]':
        filtered = List.wrap([f(a, b) for a, b in self.items()])\
            .join
        return Map(filtered)

    def bimap(self, fa: Callable[[A], C], fb: Callable[[B], D]) -> 'Map[C, D]':
        return self.map(lambda item: (fa(item[0]), fb(item[1])))

    def map2(self, f: Callable[[A, B], C]) -> List[C]:
        return List.wrap([f(a, b) for a, b in self.items()])

    @property
    def to_list(self):
        return List.wrap(self.items())

    @property
    def head(self):
        return self.to_list.head

    @property
    def keys_view(self):
        return Dict.keys(self)

    @property
    def values_view(self):
        return Dict.values(self)

    @property
    def k(self):
        return List(*Dict.keys(self))

    @property
    def v(self):
        return List(*Dict.values(self))

    @property
    def is_empty(self):
        return self.k.is_empty

    def at(self, *keys):
        return self.keyfilter(lambda a: a in keys)

    def values_at(self, *keys):
        return List.wrap(keys) // self.get

    def has_key(self, name):
        return Boolean(name in self)

    contains = has_key

__all__ = ('Map',)
