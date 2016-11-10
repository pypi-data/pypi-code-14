# -*- coding: utf-8 -*-

from setuptools import setup
from slack import __version__

setup(
    name='ltz_slack',
    version=__version__,
    install_requires=[
        "requests>=2.11.1",
        "codecov>=2.0.5",
    ],
    description="Slack API Client",
    author="Joshua",
    author_email="jongoks@gmail.com",
    scripts=[],
    url="https://github.com/jongoks/lt-slack",
    packages=["slack"],
    test_suite='tests',
)