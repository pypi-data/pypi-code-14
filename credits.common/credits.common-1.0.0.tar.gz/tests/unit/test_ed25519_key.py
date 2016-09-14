#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function

import logbook

from credits.key import ED25519SigningKey
from credits.key import ED25519VerifyingKey

logger = logbook.Logger(__name__)


def test_sk_new():
    sk = ED25519SigningKey.new()
    assert isinstance(sk, ED25519SigningKey)


def test_sk_from_string(seed_ed25519):
    sk = ED25519SigningKey.from_string(seed_ed25519)
    assert isinstance(sk, ED25519SigningKey)


def test_sk_to_string(sk_ed25519, seed_ed25519):
    assert sk_ed25519.to_string() == seed_ed25519


def test_sk_sign(sk_ed25519, payload, payload_signature_ed25519):
    assert sk_ed25519.sign(payload) == payload_signature_ed25519


def test_sk_fqdn(sk_ed25519):
    assert sk_ed25519.FQDN == "works.credits.core.ED25519SigningKey"


def test_vk_from_string(vks_ed25519):
    vk = ED25519VerifyingKey.from_string(vks_ed25519)
    assert isinstance(vk, ED25519VerifyingKey)


def test_vk_to_string(vk_ed25519, vks_ed25519):
    assert vk_ed25519.to_string() == vks_ed25519


def test_vk_verify(vk_ed25519, payload, payload_signature_ed25519):
    assert vk_ed25519.verify(payload, payload_signature_ed25519) is True


def test_vk_fqdn(vk_ed25519):
    assert vk_ed25519.FQDN == "works.credits.core.ED25519VerifyingKey"
