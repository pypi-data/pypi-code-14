#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

def publish():
    """Publish to PyPi"""
    os.system("python setup.py sdist upload")

if sys.argv[-1] == "publish":
    publish()
    sys.exit()

long_description = open('README.rst').read()

reqs = ['tornado>=4.4.2', 'docopt>=0.6.2', 'progress>=1.2']

setup(
    name='fling',
    version='0.1.1',
    description='Simple local file sharing over HTTP',
    long_description=long_description,
    author='Curtis Thompson',
    author_email='curtis@oddpost.com',
    url='http://iffius.github.com',
    packages=['fling'],
    install_requires=reqs,
    license='GPLv2',
    classifiers=(
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Version Control'),
    entry_points={
        'console_scripts': [
            'fling = fling:main'
        ]})
