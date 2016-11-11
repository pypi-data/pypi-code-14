#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    # TODO: put package requirements here
    #'psycopg2'
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='db_cache',
    version='0.1.0',
    description="database caching for dynamic programming",
    long_description=readme + '\n\n' + history,
    author="Benjamin Chiang",
    author_email='aroy@alum.mit.edu',
    url='https://github.com/bchiang2/db_cache',
    packages=[
        'db_cache',
    ],
    package_dir={'db_cache':
                 'db_cache'},
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='db_cache',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
