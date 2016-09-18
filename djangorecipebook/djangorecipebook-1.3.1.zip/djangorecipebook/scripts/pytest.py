from __future__ import absolute_import

import sys

import pytest


def main(*args):

    args = list(args) + sys.argv[1:]

    pytest.main(args or None)
