#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function

import logbook
import pytest

from credits.hash import SHA256HashProvider
from credits.hash import SHA512HashProvider

logger = logbook.Logger(__name__)


@pytest.fixture("session")
def input_string():
    return "Lorem ipsum dolor sit amet, consectetur adipiscing elit."


@pytest.fixture("session")
def output_sha256():
    return "a58dd8680234c1f8cc2ef2b325a43733605a7f16f288e072de8eae81fd8d6433"


@pytest.fixture("session")
def output_sha512():
    return "19d8350a48bb40d04b4045955a9d95599aa5bd5b8c74c36c098b58c3cd8af142b8d9cf0417ef6dc88c4ed91c69ea8e2adce7afec1afb6a21d8cae681b0902997"  # noqa


def test_sha256(input_string, output_sha256):
    assert SHA256HashProvider().hexdigest(input_string) == output_sha256


def test_sha512(input_string, output_sha512):
    assert SHA512HashProvider().hexdigest(input_string) == output_sha512
