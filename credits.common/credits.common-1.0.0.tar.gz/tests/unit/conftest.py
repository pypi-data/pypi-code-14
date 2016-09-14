#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function

import logbook
import pytest

from credits.address import CreditsAddressProvider
from credits.hash import SHA256HashProvider
from credits.key import ED25519SigningKey

logger = logbook.Logger(__name__)


@pytest.fixture("session")
def hash_provider():
    return SHA256HashProvider()


@pytest.fixture("session")
def payload():
    return "exampletestpayload"


@pytest.fixture("session")
def payload_signature_ed25519():
    return "ed3de3b3522bb689301cb39dc1e0bd9882d071a76c06e4d51a71244bed375fc3742ea214c9a3b2605d1f3695861c9f5ffce66a8543aa66d3b8bcb1a21e6e2f02"  # noqa


@pytest.fixture("session")
def seed_ed25519():
    return "9a653f45feccaaa8f4a8de5706a426144905079eace300a03d9b77b5019cad65"  # seed not actual bytes


@pytest.fixture("session")
def vks_ed25519():
    return "376d4825d62da147776dfad690ccc0491ccc2474bf75073aeadb2788613b2d8d"


@pytest.fixture("session")
def address_ed25519():
    return "1DrVHK6tbH4t7ZDAUFrFr7MvnvZmBBGL8R"


@pytest.fixture("session")
def sk_ed25519(seed_ed25519):
    return ED25519SigningKey.from_string(seed_ed25519)


@pytest.fixture("session")
def vk_ed25519(sk_ed25519):
    return sk_ed25519.get_verifying_key()


@pytest.fixture("session")
def ed25519_one():
    return ED25519SigningKey.from_string("9a821e7288275ddc8ed286757f23dc5310d62d7c22fa67cd896e50abb972a8a2")


@pytest.fixture("session")
def ed25519_two():
    return ED25519SigningKey.from_string("4f20230423732538cd093b3f0d591be5690d04eca6da4fba527e72520f613790")


@pytest.fixture("session")
def ed25519_one_address(ed25519_one):
    # 1JLHUyiH7NjsAGJxuD1YpJ8XEogd7gxJen
    return CreditsAddressProvider(ed25519_one.get_verifying_key().to_string()).get_address()


@pytest.fixture("session")
def ed25519_two_address(ed25519_two):
    # 12dtJyqYHa4p1Tg2cR8coUPvy7sJcUNvoY
    return CreditsAddressProvider(ed25519_two.get_verifying_key().to_string()).get_address()
