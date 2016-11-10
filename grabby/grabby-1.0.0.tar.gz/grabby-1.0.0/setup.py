#!/usr/bin/env python
import os
import shutil
import sys
from setuptools import setup, find_packages

# Bump pyglet/__init__.py version as well.
VERSION = '1.0.0'

long_description = '''
Grabby is a command line tool / python module that allows you to copy directory trees from any OS based on user defined filters.
'''

setup_info = dict(
    # Metadata
    name='grabby',
    version=VERSION,
    author='Michael Green',
    author_email='me@michaelgreen.net',
    url='http://michaelgreen.net',
    download_url='http://pypi.python.org/pypi/grabby',
    description='A tool to easily copy directory trees while excluding or including certain files with regular expression filters.',
    long_description=long_description,
    license='GPL',
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4'
    ]
)

setup(**setup_info)
