#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from setuptools import setup

with open('downloadbuffer/__init__.py', 'r') as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError('Cannot find version')


with open('README.rst', 'r') as f:
    readme = f.read()

packages = [
    'downloadbuffer'
]

requires = [
    'requests',
    'queueio'
]

setup(
    name = 'downloadbuffer',
    author = 'Nick Anderegg',
    author_email = 'nick@anderegg.io',
    version = version,
    license = 'GPLv3',
    description = 'Stream and buffer large files via HTTP',
    long_description = readme,
    url = 'https://github.com/NickAnderegg/downloadbuffer',
    packages = packages,
    package_data = {'': ['LICENSE']},
    package_dir = {'downloadbuffer': 'downloadbuffer'},
    include_package_data = True,
    install_requires = requires,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: Implementation :: CPython'
    ]
)
