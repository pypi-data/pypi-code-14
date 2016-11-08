#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function

import abc


class Marshallable(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def marshall(self):
        """
        Convert this class into a primitive map.
        """

    @classmethod
    @abc.abstractmethod
    def unmarshall(cls, registry, payload):
        """
        Take a primitive map and restore it into an instance.
        """


class Applicable(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def verify(self, state):
        """
        Verify this object against a given state. Throw exception if not valid.

        :type state: credits.state.State
        """

    @abc.abstractmethod
    def apply(self, state):
        """
        Apply this object to the state, mutate the state and return it.

        :type state: credits.state.State
        :rtype state: credits.state.State
        """


class Signable(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def sign(self, signing_key):
        """
        Sign this object based on it's contents. Then return a new instance of the object with it's signature and
        verifying_key.

        :type signing_key: credits.key.SigningKey

        :returns: A signature of the contents of this object.
        :rtype: self
        """


class Hashable(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def hash(self, hash_provider):
        """
        Hash this object based on it's contents. Then return a new instance of the object with it's hash.
        :type hash_provider: credits.hash.HashProvider

        :returns: A signature of the contents of this object.
        :rtype: self
        """


class Transactional(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def rollback(self):
        """
        Revert the unconfirmed changes to this Transactional object.
        """

    @abc.abstractmethod
    def commit(self):
        """
        Commit the unconfirmed changes to this Transactional object.
        """
