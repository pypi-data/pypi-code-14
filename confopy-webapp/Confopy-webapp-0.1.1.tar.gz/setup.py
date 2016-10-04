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

def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)

setup(
    name='Confopy-webapp',
    version='0.1.1',
    url='https://github.com/ooz/Confopy-webapp',
    author='Oliver Zscheyge',
    description='Minimal web UI for Confopy.',
    long_description=read('README.md'),
    license='MIT',
    author_email='oliverzscheyge@gmail.com',
    packages=['confopyapp'],
    package_data={'': ['README.md', 'LICENSE']},
    data_files = ["README.md"],
    include_package_data=True,
    install_requires=['Flask==0.11.1'],
    classifiers=(
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    )
)
