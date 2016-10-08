#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
import sys

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    # TODO: put package requirements here
    'Pillow==2.8',
    'requests>=1.0',
    'ipython',
    'jupyter',
] + ["sh"] if "Darwin" in sys.platform else []

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='pypathway',
    version='0.1.2',
    description="A Python package for playing with pathways",
    long_description=readme + '\n\n' + history,
    author="sheep",
    author_email='sss3barry@gmail.com',
    url='https://github.com/iseekwonderful/pypathway',
    packages=[
        'pypathway',
    ],
    package_dir={'pypathway':
                 'pypathway'},
    include_package_data=True,
    install_requires=requirements,
    license="GNU General Public License v3",
    zip_safe=False,
    keywords='pypath',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
