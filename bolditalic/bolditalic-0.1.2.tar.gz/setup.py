#!/bin/python3
# coding: utf-8
"""bolditalic setup file."""

# To use a consistent encoding
from codecs import open
from os import path

from setuptools import setup

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='bolditalic',
    version='0.1.2',
    description='A Sphinx extension that enables inline bold + italic.',
    long_description=long_description,
    url='https://github.com/kallimachos/bolditalic',
    author='Brian moss',
    author_email='kallimachos@gmail.com',
    license='GPLv3',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Documentation :: Sphinx',
        'Framework :: Sphinx :: Extension',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
    ],

    keywords='sphinx documentation bold italic',
    packages=['bolditalic'],

    package_data={
        'bolditalic': ['bolditalic.css'],
    },
)
