#!/usr/bin/env python

import os
import re
import sys
from codecs import open

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


if sys.argv[-1] == 'publish':
    os.system('python setup.py register')
    os.system('python setup.py sdist upload')
    sys.exit()

setup(
    name='Confopy-webapp',
    version='0.1.4',
    url='https://github.com/ooz/Confopy-webapp',
    author='Oliver Zscheyge',
    description='Minimal web UI for Confopy.',
    long_description=open('README.md').read(),
    license='MIT',
    author_email='oliverzscheyge@gmail.com',
    packages=['confopyapp'],
    package_data={'': ['README.md', 'LICENSE']},
    data_files=["README.md"],
    include_package_data=True,
    install_requires=['Flask==0.11.1']
)
