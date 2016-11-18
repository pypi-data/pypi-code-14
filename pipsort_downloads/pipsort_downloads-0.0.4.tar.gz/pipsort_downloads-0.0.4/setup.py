#!/usr/bin/env python
# encoding: utf-8

import codecs
import os
import sys
 
try:
    from setuptools import setup
except:
    from distutils.core import setup
 
def read(fname):
    """
    Searh python package from pypi and sort them by their donwloads
    """
    return codecs.open(os.path.join(os.path.dirname(__file__), fname)).read()
 
 
 
NAME = "pipsort_downloads"
PACKAGES = []
DESCRIPTION = "Searh package from pypi sorted by their donwloads"
 
LONG_DESCRIPTION = read("README.rst")
KEYWORDS = "search package downloads sorted"
AUTHOR = "catlovemouse"
AUTHOR_EMAIL = "liyongjie1982@email.com"
URL = "https://pypi.python.org/pypi/pipsort_downloads"
VERSION = "0.0.4"
LICENSE = "MIT"
 
setup(
    name = NAME,
    version = VERSION,
    description = DESCRIPTION,
    long_description = LONG_DESCRIPTION,
    classifiers = [
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
    ],
    keywords = KEYWORDS,
    author = AUTHOR,
    author_email = AUTHOR_EMAIL,
    url = URL,
    license = LICENSE,
    packages = PACKAGES,
    include_package_data=True,
    zip_safe=True,
    scripts=['bin/pipsort'],
)
 
