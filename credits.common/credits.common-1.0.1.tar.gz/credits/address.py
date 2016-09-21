#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function

from hashlib import sha256

import logbook
from base58 import b58encode

logger = logbook.Logger(__name__)


class AddressProvider(object):
    """
    AddressProvider is an abstraction allowing any string to be converted into an "Address".
    Address should have hash like properties of providing deterministic output for a given input and being
    non-reversable.
    """

    def get_address(self):
        raise NotImplementedError()


class CreditsAddressProvider(AddressProvider):
    def __init__(self, value):
        """
        An AddressProvider using an in-house algorithm based off double sha256 and base58 encoding.

        :type input_str: str
        """
        self.value = value

    def get_address(self):
        """
        Generate an address from self.input_str. This is typically performed using a verifying key.

        :rtype: str
        """
        digest = "00" + sha256(self.value).hexdigest()[:40]
        checksum = sha256(sha256(digest).hexdigest()).hexdigest()[:8]
        address = digest + checksum

        return b58encode(address.decode("hex"))
