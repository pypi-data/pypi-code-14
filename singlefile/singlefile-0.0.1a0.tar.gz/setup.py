#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

version = '0.0.1.alpha0'
packages = ['singlefile']
install_requires = [
    'requests'
]
classifiers = [
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Natural Language :: English',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3 :: Only',
    'Programming Language :: Python :: Implementation :: CPython',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Topic :: Utilities'
]

config = {
    'description': 'import from web. share your snippets and import them from web',
    'author': 'Srinivas Devaki',
    'url': 'https://gitlab.com/eightnoteight/singlefile',
    'download_url': 'https://gitlab.com/eightnoteight/singlefile/repository/archive.zip?ref=master',
    'author_email': 'mr.eightnoteight@gmail.com',
    'version': version,
    'install_requires': install_requires,
    'packages': packages,
    'scripts': [],
    'classifiers': classifiers,
    'name': 'singlefile'
}

setup(**config)
