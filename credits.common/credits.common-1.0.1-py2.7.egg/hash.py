#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function

import abc
import hashlib

import logbook

from credits.interface import Marshallable


class HashProvider(Marshallable):
    __metaclass__ = abc.ABCMeta

    fqdn = "NOTSET"

    def __init__(self):
        self.logger = logbook.Logger(__name__)

    @abc.abstractmethod
    def hexdigest(self, i):
        """
        Given a string input of 'i', return a cryptographic hash of it's contents.
        """


class SHA256HashProvider(HashProvider):
    fqdn = "works.credits.core.SHA256HashProvider"

    def hexdigest(self, i):
        """
        Return the SHA256 digest of the input i.

        :type i: str
        :rtype: str
        """
        return hashlib.sha256(i).hexdigest()

    def marshall(self):
        return {
            "fqdn": self.fqdn,
        }

    @classmethod
    def unmarshall(cls, registry, payload):
        return cls()


class SHA512HashProvider(HashProvider):
    fqdn = "works.credits.core.SHA512HashProvider"

    def hexdigest(self, i):
        """
        Return the SHA512 digest of the input i.

        :type i: str
        :rtype: str
        """
        return hashlib.sha512(i).hexdigest()

    def marshall(self):
        return {
            "fqdn": self.fqdn,
        }

    @classmethod
    def unmarshall(cls, registry, payload):
        return cls()
