#!/usr/bin/env python3
# -*- coding: utf8 -*-
from setuptools import find_packages, setup

setup(
    name='sites',
    version='0.0.1',
    author='Joaquín Sorianello',
    author_email='joac@joac.com',
    long_description='sites provides a framework for building url based sites',
    packages=find_packages(exclude=["tests", "examples"]),
    license="?",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ],
    install_requires=[
        'werkzeug',
        'aiocoap',
        'aiohttp',
    ],
)
