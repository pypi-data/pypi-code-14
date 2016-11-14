#!/usr/bin/env python

from setuptools import setup

setup(
    name="nfq",
    description="NFQ Solutions base package",
    version="0.1.1",
    author="NFQ Solutions",
    author_email="solutions@nfq.es",
    packages=[
        'nfq',
        ],
    zip_safe=False,
    setup_requires=['pytest-runner'],
    tests_require=['pytest']
    )
