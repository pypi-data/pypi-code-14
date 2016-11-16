#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
    def digest(self, i):
        """
        Given a string input of 'i', return a cryptographic hash of it's contents.
        """


class SHA256HashProvider(HashProvider):
    fqdn = "works.credits.core.SHA256HashProvider"

    def digest(self, i: bytes) -> bytes:
        """
        Return the SHA256 digest of the input i.

        :type i: bytes
        :rtype: bytes
        """
        return hashlib.sha256(i).digest()

    def marshall(self) -> dict:
        return {
            "fqdn": self.fqdn,
        }

    @classmethod
    def unmarshall(cls, registry, payload):
        return cls()


class SHA512HashProvider(HashProvider):
    fqdn = "works.credits.core.SHA512HashProvider"

    def digest(self, i: bytes) -> bytes:
        """
        Return the SHA512 digest of the input i.

        :type i: bytes
        :rtype: str
        """
        return hashlib.sha512(i).digest()

    def marshall(self) -> dict:
        return {
            "fqdn": self.fqdn,
        }

    @classmethod
    def unmarshall(cls, registry, payload):
        return cls()
