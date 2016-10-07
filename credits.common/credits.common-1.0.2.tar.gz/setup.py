#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function

import setuptools

version = "1.0.2"

packages = [
    "base58==0.2.2",
    "ed25519",
    "logbook==0.12.5",
]

setuptools.setup(
    name="credits.common",
    version=version,
    author="Credits Developers",
    author_email="admin@credits.vision",
    install_requires=packages,
    namespace_packages=['credits'],
    packages=setuptools.find_packages(),
    url="https://github.com/CryptoCredits/credits-common",
    download_url="https://github.com/CryptoCredits/credits-common/tarball/%s" % version,
)
