#!/usr/bin/env python
#
# Copyright (c) 2016 BlueData Software, Inc.
#
from distutils.core import setup
from setuptools import find_packages

import bdworkbench

setup(
    name = 'bdworkbench',
    packages = find_packages(),
    version = bdworkbench.__version__,
    description = 'Appstore SDK for BlueData EPIC platform.',
    author = 'BlueData Software, Inc.',
    author_email = 'krishna@bluedata.com',
    url = 'https://github.com/bluedatainc/catalogsdk',
    keywords = [ 'BlueData', 'appstore', 'catalog', 'EPIC'],
    entry_points = {
        "console_scripts" : [ 'bdwb=bdworkbench.__main__:main' ],
    },
    install_requires = [
        'argparse',
        'requests'
    ],
    classifiers = [
            "Environment :: Console",
            "Programming Language :: Python",
    ]
)
