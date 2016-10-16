#!/usr/bin/env python
# -*- coding:utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
import os
from setuptools import setup, find_packages

readme = 'Send message to Line.app'
if os.path.exists('README.txt'):
    readme = open('README.txt').read()


def _requires_from_file(filename):
    return open(filename).read().splitlines()

# version
here = os.path.dirname(os.path.abspath(__file__))
version = next((line.split('=')[1].strip().replace("'", '')
                for line in open(os.path.join(here,
                                              'lipy_notify',
                                              '__init__.py'))
                if line.startswith('__version__ = ')),
               '0.0.1')

setup(
    name="lipy_notify",
    version=version,
    url='https://github.com/butsugiri',
    author='shunk52',
    author_email='shunk52@gmail.com',
    description='Post message to LINE.app from python',
    long_description=readme,
    packages=find_packages(),
    license="MIT",
    classifiers=[
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'License :: OSI Approved :: MIT License',
    ],
    install_requires=[
        "requests"
    ],
)
