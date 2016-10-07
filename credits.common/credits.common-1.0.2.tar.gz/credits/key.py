#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function

import ed25519
import logbook

from credits.interface import Marshallable


class SigningKey(Marshallable):
    fqdn = "NOTSET"

    def __init__(self):
        self.logger = logbook.Logger(__name__)

    @classmethod
    def new(cls):
        raise NotImplementedError()

    @classmethod
    def from_string(cls, sk_s):
        raise NotImplementedError()

    def to_string(self):
        raise NotImplementedError()

    def get_verifying_key(self):
        raise NotImplementedError()

    def sign(self, data):
        raise NotImplementedError()

    def __str__(self):
        return self.to_string()


class VerifyingKey(Marshallable):
    fqdn = "NOTSET"

    def __init__(self):
        self.logger = logbook.Logger(__name__)

    @classmethod
    def from_string(cls, sk_s):
        raise NotImplementedError()

    def to_string(self):
        raise NotImplementedError()

    def verify(self, data, signature):
        raise NotImplementedError()

    def __str__(self):
        return self.to_string()


class ED25519VerifyingKey(VerifyingKey):
    fqdn = "works.credits.core.ED25519VerifyingKey"

    def __init__(self, vk):
        super(ED25519VerifyingKey, self).__init__()
        self.vk = vk

    @classmethod
    def unmarshall(cls, registry, payload):
        return cls.from_string(payload["vks"])

    def marshall(self):
        return {
            "fqdn": self.fqdn,
            "vks": self.to_string(),
        }

    @classmethod
    def from_string(cls, vks):
        """
        Take the output from ED25519VerifyingKey.to_string and convert it back into a VerifyingKey.

        :type sks: str
        :rtype: credits.key.ED25519VerifyingKey
        """
        vk = ed25519.VerifyingKey(vks.decode("hex"))
        return cls(vk)

    def to_string(self):
        """
        Generate a string representation of this verifying key, useful for generating addresses using an AddressProvider

        :rtype: str
        """
        return self.vk.to_ascii(encoding="hex")

    def verify(self, data, signature):
        """
        Verify data with a provided signature.

        :type data: str
        :type signature: str
        :return: bool
        """
        try:
            self.vk.verify(signature.decode("hex"), data.encode("utf-8"))
            return True
        except ed25519.BadSignatureError:
            return False


class ED25519SigningKey(SigningKey):
    fqdn = "works.credits.core.ED25519SigningKey"

    def __init__(self, sk):
        super(ED25519SigningKey, self).__init__()
        self.sk = sk

    @classmethod
    def unmarshall(cls, registry, payload):
        return cls.from_string(payload["sks"])

    def marshall(self):
        return {
            "fqdn": self.fqdn,
            "sks": self.to_string(),
        }

    @classmethod
    def new(cls):
        """
        Generate a new ED25519SigningKey.

        :rtype: credits.key.ED25519SigningKey
        """
        sk, _ = ed25519.create_keypair()
        return cls(sk)

    @classmethod
    def from_string(cls, sks):
        """
        Take the output from ED25519SigningKey.to_string and convert it back into a SigningKey.

        :type sks: str
        :rtype: credits.key.ED25519SigningKey
        """
        sk = ed25519.SigningKey(sks.decode("hex"))
        return cls(sk)

    def to_string(self):
        return self.sk.to_ascii(encoding="hex")

    def get_verifying_key(self):
        """
        Generate the complementary ED25519VerifyingKey from this ED25519SigningKey.

        :rtype: ED25519VerifyingKey
        """
        return ED25519VerifyingKey(self.sk.get_verifying_key())

    def sign(self, data):
        """
        Sign a string with this ED25519SigningKey.

        :type data: str
        :return: str
        """
        return self.sk.sign(str(data)).encode("hex")
