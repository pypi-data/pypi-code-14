# Copyright (c) Aaron Gallagher <_@habnab.it>
# See COPYING for details.

import tcversioner

# not this again
from setuptools import setup


with open('README.rst', 'r') as infile:
    long_description = infile.read()

setup(
    name='tcversioner',
    version=tcversioner.find_version().version,
    description='Use version control tags to discover version numbers',
    long_description=long_description,
    author='Tyler Crumpton',
    author_email='tyler.crumpton@gmail.com',
    url='https://github.com/tylercrumpton/vcversioner',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Version Control',
    ],
    license='ISC',

    py_modules=['tcversioner'],
    entry_points={
        'distutils.setup_keywords': ['tcversioner = tcversioner:setup'],
    },
)
