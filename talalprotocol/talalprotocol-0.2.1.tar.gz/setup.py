#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    # TODO: put package requirements here
    'wheel==0.29',
    'pip==8.1.2',
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='talalprotocol',
    version='0.2.1',
    description="Deep Layered Encryption",
    long_description=readme + '\n\n' + history,
    author="Team Standy",
    author_email='teamstandyy@gmail.com',
    url='https://github.com/s3nu/talalprotocol',
    license='Team Standy License',
    packages=[
        'talalprotocol',
    ],
    package_dir={'talalprotocol':
                 'talalprotocol'},
    include_package_data=True,
    install_requires=requirements,
    zip_safe=False,
    keywords='encryption talalprotocol python3',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: MacOS',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ]
    #test_suite='tests',
    #tests_require=test_requirements
)
