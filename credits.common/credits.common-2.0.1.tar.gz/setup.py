#!/usr/bin/env python
# -*- coding: utf-8 -*-
import setuptools

version = "2.0.1"

packages = [
    "base58==0.2.2",
    "logbook==0.12.5",
    "ed25519",  # specifically unversioned
]

setuptools.setup(
    name="credits.common",
    version=version,
    author="Credits Developers",
    author_email="admin@credits.vision",
    description="Credits blockchain framework common client library",
    install_requires=packages,
    namespace_packages=['credits'],
    packages=setuptools.find_packages(),
    url="https://github.com/CryptoCredits/credits-common",
    download_url="https://github.com/CryptoCredits/credits-common/tarball/%s" % version,
)
