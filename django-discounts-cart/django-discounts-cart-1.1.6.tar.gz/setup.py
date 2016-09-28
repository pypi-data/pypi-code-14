#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Copyright (c) 2016 genkosta
#
#  django-discounts-cart is free software under terms of the MIT License.
#

import os
import re
from codecs import open as codecs_open
from setuptools import setup, find_packages


def read(*parts):
    file_path = os.path.join(os.path.dirname(__file__), *parts)
    return codecs_open(file_path, encoding='utf-8').read()


def find_version(*parts):
    version_file = read(*parts)
    version_match = re.search(
        r'''^__version__ = ['"]([^'"]*)['"]''', version_file, re.M)
    if version_match:
        return str(version_match.group(1))
    raise RuntimeError('Unable to find version string.')


setup(
    name     = 'django-discounts-cart',
    version  = find_version('discounts_cart', '__init__.py'),
    packages= find_packages(),
    requires = ['python (== 2.7)', 'django (>= 1.7)'],
    description  = 'Discounts for online store and management cart',
    long_description = open('README.rst').read(),
    author       = 'genkosta',
    author_email = 'genkosta43@gmail.com',
    url          = 'https://github.com/genkosta/django-discounts-cart',
    download_url = 'https://github.com/genkosta/django-discounts-cart/tarball/master',
    license      = 'MIT License',
    keywords     = 'django discounts cart commerce e-ecommerce',
    classifiers  = [
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],
)
