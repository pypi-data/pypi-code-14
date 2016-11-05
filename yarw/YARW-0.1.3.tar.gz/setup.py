#!/usr/bin/env python

import os
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

BASE_DIR = os.path.dirname(__file__)
README_PATH = os.path.join(BASE_DIR, 'README.md')
VERSION_PATH = os.path.join(BASE_DIR, 'VERSION')
LICENSE_PATH = os.path.join(BASE_DIR, 'LICENSE')
DESCRIPTION = open(README_PATH).read()
VERSION = open(VERSION_PATH).read()
LICENSE = open(LICENSE_PATH).readline().strip()

setup(
    name='YARW',
    version=VERSION,
    description='Yet Another Registry Wrapper.',
    long_description=DESCRIPTION,
    author='Mars Galactic',
    author_email='xoviat@github.com',
    url='https://github.com/xoviat/YARW',
    py_modules=['YARW'],
    license=LICENSE,
    platforms='any',
    keywords=['registry'],
    classifiers=[],
    )
