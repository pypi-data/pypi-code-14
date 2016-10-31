# Copyright 2014-2016 Morgan Delahaye-Prat. All Rights Reserved.
#
# Licensed under the Simplified BSD License (the "License");
# you may not use this file except in compliance with the License.
"""Implements the base model."""


import inspect


class BaseModel:
    """Base class of all models."""

    @classmethod
    def _key(cls):
        """Get the key of a model.

        The key is a set of properties used to determine the unique identifier
        of a resource.

        Returns:
            a tuple.
        """
        if not hasattr(cls, '__key__'):  # pragma: no cover
            raise NotImplementedError()

        rv = cls.__key__
        if not isinstance(rv, tuple):   # ensure the returned value is a tuple
            rv = rv,

        return rv

    @property
    def _uid(self):
        """Get the unique identifier of a resource.

        The unique identifier (uid) of a resource is a set of values unique to
        each instance of a model.

        Returns:
            a tuple.
        """
        return tuple(getattr(self, k) for k in self._key())

    @classmethod
    def get(cls, _offset, _limit, **kwargs):  # pragma: no cover
        """Get a list of resources."""
        raise NotImplementedError()

    @classmethod
    def count(cls, **kwargs):
        """Get the number of resources."""
        # This is a basic and not optimized method based on get()
        return len(cls.get(**kwargs))

    @classmethod
    def one(cls, *args):
        """Get one resource."""
        # This is a basic and not optimized method based on get()
        rv = cls.get(**{k: v for k, v in zip(cls._key(), args)})
        if len(rv) == 1:
            return rv[0]

    def save(self, commit=True):  # pragma: no cover
        """Make the resource persistent in the data store.

        Args:
            commit: commit inline.
        """
        raise NotImplementedError()

    def delete(self):  # pragma: no cover
        """Delete the resource from the data store.

        Args:
            commit: commit inline.
        """
        raise NotImplementedError()

    @classmethod
    def commit(cls):  # pragma: no cover
        """Commit changes."""
        raise NotImplementedError()

    @classmethod
    def rollback(cls):  # pragma: no cover
        """Rollback changes.

        The rollback is usable on the pending or failed commits.
        """
        pass

    def __serialize__(self, context=None):
        """Serialize the instance.

        Args:
            context: change the behaviour of the serialization process.
        """
        return {k: v for k, v in inspect.getmembers(self)
                if not k.startswith('_') and not inspect.isroutine(v)}
