# Copyright 2016 Allen Li
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Abstract base classes for mir.monads package."""

import abc

import mir.monads.fun as fun


class Functor(abc.ABC):

    """Functor supertype

    class Functor f where
        fmap :: (a -> b) -> f a -> f b

    The argument order of fmap() is flipped from Haskell as it is now a method.
    """

    @abc.abstractmethod
    def fmap(self, f):
        """Map a function over the functor."""
        raise NotImplementedError


class Applicative(Functor):

    """Applicative supertype

    class (Functor f) => Applicative f where
        pure :: a -> f a
        (<*>) :: f (a -> b) -> f a -> f b

    Implemented methods:
    apply -- (<*>)
    """

    @abc.abstractmethod
    def apply(self, other):
        """Apply the applicative to another applicative."""
        raise NotImplementedError


class Monad(Applicative):

    """Monad supertype

    class Monad m where
        (>>=) :: m a -> (a -> m b) -> m b
        (>>) :: m a -> m b -> m b
        return :: a -> m a
        fail :: String -> m a

    Implemented methods:
    bind -- (>>=)
    """

    @abc.abstractmethod
    def bind(self, f):
        """Apply a function to the monad."""
        raise NotImplementedError

    def __rshift__(self, f):
        return self.bind(f)


@fun.curry
def kleisli_compose(f: Monad, g: Monad, h):
    """Kleisli composition operator

    Denoted >=> in Haskell.
    """
    return f(h) >> g
