from typing import TypeVar, Callable, Tuple

from amino import _, Maybe, LazyList
from amino.list import List
from amino.func import F, curried
from amino.anon import __
from amino.tc.functor import Functor
from amino.tc.base import ImplicitInstances, tc_prop
from amino.lazy import lazy
from amino.tc.traverse import Traverse
from amino.tc.foldable import Foldable

A = TypeVar('A')
B = TypeVar('B')


class LazyListInstances(ImplicitInstances):

    @lazy
    def _instances(self):
        from amino.map import Map
        return Map(
            {
                Functor: LazyListFunctor(),
                Traverse: LazyListTraverse(),
                Foldable: LazyListFoldable(),
            }
        )


class LazyListFunctor(Functor):

    def pure(self, a: A):
        return LazyList([], List(a))

    def map(self, fa: LazyList[A], f: Callable[[A], B]) -> LazyList[B]:
        return LazyList(map(f, fa.source), fa.strict, fa._chunk_size)


class LazyListTraverse(Traverse):

    def traverse(self, fa: LazyList[A], f: Callable, tpe: type):
        return fa.drain.traverse(f, tpe) / LazyList


class LazyListFoldable(Foldable):

    @tc_prop
    def with_index(self, fa: LazyList[A]) -> List[Tuple[int, A]]:
        return LazyList(enumerate(fa.source), fa.strict, fa._chunk_size)

    def filter(self, fa: LazyList[A], f: Callable[[A], bool]):
        return fa.copy(F(filter, f), __.filter(f))

    @curried
    def fold_left(self, fa: LazyList[A], z: B, f: Callable[[B, A], B]) -> B:
        return Foldable[List].fold_left(fa.drain, z, f)

    def find(self, fa: List[A], f: Callable[[A], bool]):
        return fa.strict.find(f) | fa._drain_find(f)

    def find_map(self, fa: LazyList[A], f: Callable[[A], Maybe[B]]
                 ) -> Maybe[B]:
        return fa.map(f).find(_.is_just)

    def index_where(self, fa: LazyList[A], f: Callable[[A], bool]
                    ) -> Maybe[int]:
        return fa.strict.index_where(f) | (
            fa._drain_find(f) / (lambda a: len(fa.strict) - 1))

__all__ = ('LazyListInstances',)
