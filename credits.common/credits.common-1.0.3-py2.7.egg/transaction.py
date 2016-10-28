#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function

import logbook

from credits.interface import Applicable
from credits.interface import Hashable
from credits.interface import Marshallable
from credits.stringify import stringify


class Transaction(Marshallable, Applicable, Hashable):
    fqdn = "works.credits.core.Transaction"

    def __init__(self, transform, proofs):
        """
        :type transform: credits.transform.Transform
        :type proofs: {str: credits.proof.Proof}
        :type digest: str
        """
        self.logger = logbook.Logger(__name__)

        self.transform = transform
        self.proofs = proofs

    # interface.Applicable
    def verify(self, state):
        """
        Perform validation of transform and proofs against a given state. Raise ValidationException if not valid.

        :param state: The state to be validated.
        :type state: credits.state.State
        """
        if len(self.proofs) == 0:
            error = "Invalid Transaction: tx contains no proofs to validate against."
            self.logger.error(error)
            return None, error

        # Make sure that the required auths are a subset of all proofs in this transaction.
        if not set(self.transform.required_authorizations()).issubset(set(self.proofs)):
            error = "Required Authorizations for this Transaction are not met."
            self.logger.error(error)
            return None, error

        for address, proof in self.proofs.items():
            # Check the proof is valid.
            result, error = proof.verify(state)
            if error is not None:
                return None, error

            # Now check k == v for proofs by asking for the address the proof is associated with.
            if address != proof.address:
                error = "A proof for address %s does not contain an associated signature." % (address,)
                self.logger.error(error)
                return None, error

        result, error = self.transform.verify(state)
        if error is not None:
            return None, error

        return state, None

    # interface.Applicable
    def apply(self, state):
        """
        Applies the transform, then the proofs. If all things apply correctly return the new state.

        :param state: The state to be modified.
        :type state: credits.state.State

        :rtype: credits.state.State
        """
        # Apply Proofs
        for proof in self.proofs.values():
            result, error = proof.apply(state)

            if error is not None:
                return None, error

        # Apply Transform
        result, error = self.transform.apply(state)
        if error is not None:
            return None, error

        return state, None

    def hash(self, hash_provider):
        items = [
            self.transform.get_challenge(hash_provider),
        ]

        for address, proof in self.proofs.items():
            items.append(address)
            items.append(proof.nonce)

        data = stringify(items)

        return hash_provider.hexdigest(data)

    # interface.Marshallable
    def marshall(self):
        proofs = {}
        for address, proof in self.proofs.items():
            proofs[address] = proof.marshall()

        return {
            "fqdn": self.fqdn,
            "transform": self.transform.marshall(),
            "proofs": dict((address, proof.marshall()) for address, proof in self.proofs.items()),
        }

    # interface.Marshallable
    @classmethod
    def unmarshall(cls, registry, payload):
        transform = registry.unmarshall(payload["transform"])
        proofs = dict((address, registry.unmarshall(proof)) for address, proof in payload["proofs"].items())

        return cls(
            transform=transform,
            proofs=proofs,
        )
