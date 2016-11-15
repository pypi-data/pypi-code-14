# -*- coding: utf-8 -*-
import os
import sys
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup, Extension
from distutils.core import Extension
from distutils.errors import DistutilsError
from distutils.command.build_ext import build_ext

with open(os.path.join('syncache', '__init__.py')) as f:
    exec(f.read())

tests_require = []
install_requires = []
setup_requires = []

setup(
    name='syncache',
    version=__version__,
    packages=['syncache'],
    ext_modules=[],
    tests_require=tests_require,
    install_requires=install_requires,
    setup_requires=setup_requires,
    description='Synchronization Cache for Grid Computing',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
    ],
    author=__author__,
    author_email=__email__,
    url='https://github.com/pakozm/syncache',
    download_url='https://github.com/pakozm/syncache/tarball/0.2.1',
    keywords=['rsync', 'cache'],
    license=__license__,
    test_suite="nose.collector",
)
