#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function

import logbook

from credits.address import CreditsAddressProvider
from credits.interface import Applicable
from credits.interface import Marshallable
from credits.interface import Signable


class Proof(Marshallable, Applicable, Signable):
    def __init__(self):
        self.logger = logbook.Logger(__name__)


class SingleKeyProof(Proof):
    fqdn = 'works.credits.core.SingleKeyProof'

    STATE_NONCE = "works.credits.core.IntegerNonce"

    def __init__(self, address, nonce, challenge, verifying_key=None, signature=None):
        """
        Sign a challenge. This signature can be used as a proof.

        :type registry: credits.registry.ComponentRegistry
        :type address: str
        :type nonce: int
        :type challenge: str
        :type verifying_key: credits.key.VerifyingKey
        :type signature: str
        """
        super(SingleKeyProof, self).__init__()

        self.address = address
        self.nonce = nonce
        self.challenge = challenge

        self.verifying_key = verifying_key
        self.signature = signature

    def verify(self, state):
        """
        Verify this proof has been signed and that it's signature/verifying_key/challenge is valid against state.

        :returns: result, error
        """
        if (self.signature is None) or (self.verifying_key is None):
            error = "Proof has not been signed."
            self.logger.error(error)
            return None, error

        address = CreditsAddressProvider(self.verifying_key.to_string()).get_address()

        if address != self.address:
            error = "Proof for address %s was signed with %s" % (self.address, address)
            self.logger.error("Proof for address %s was signed with %s" % (self.address, address))
            return None, error

        if not self.verifying_key.verify(self.challenge, self.signature):
            error = "SingleKeyProof failed a signature check against %s" % address
            self.logger.error(error)
            return None, error

        known_nonce = state[self.STATE_NONCE][address]
        if self.nonce < known_nonce:
            error = "SingleKeyProof nonce (%s) is less than current nonce (%s) for %s" % (self.nonce, known_nonce,
                                                                                          address)
            self.logger.error(error)
            return None, error

        return state, None

    def apply(self, state):
        """
        Increment nonce of the associated address. this operation should assume the address potentially doesn't exist so
        this operation should be performed safely.
        """
        address = CreditsAddressProvider(self.verifying_key.to_string()).get_address()
        nonces = state[self.STATE_NONCE]

        if self.nonce != nonces.get(address, 0):
            error = "SingleKeyProof nonce (%s) is not equal to nonce (%s) for %s" % (
                self.nonce,
                nonces.get(address, 0),
                address
            )
            self.logger.error(error)
            return None, error

        nonces[address] = nonces.get(address, 0) + 1

        return state, None

    def sign(self, signing_key):
        """
        Sign this proof.

        :type signing_key: credits.key.SigningKey
        :rtype: credits.proof.SingleKeyProof
        """
        verifying_key = signing_key.get_verifying_key()
        signature = signing_key.sign(self.challenge)

        return SingleKeyProof(
            address=self.address,
            nonce=self.nonce,
            challenge=self.challenge,
            verifying_key=verifying_key,
            signature=signature,
        )

    def marshall(self):
        verifying_key = None
        if self.verifying_key is not None:
            verifying_key = self.verifying_key.marshall()

        return {
            "fqdn": self.fqdn,
            "address": self.address,
            "nonce": self.nonce,
            "challenge": self.challenge,
            "verifying_key": verifying_key,
            "signature": self.signature,
        }

    @classmethod
    def unmarshall(cls, registry, payload):
        return cls(
            address=payload["address"],
            nonce=payload["nonce"],
            challenge=payload["challenge"],
            verifying_key=registry.unmarshall(payload["verifying_key"]),
            signature=payload["signature"],
        )
