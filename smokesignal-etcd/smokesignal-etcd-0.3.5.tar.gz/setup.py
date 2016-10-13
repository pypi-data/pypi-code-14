#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

with open('requirements.txt') as req_file:
	requirements = [x for x in req_file.read().split('\n')]

with open('requirements_dev.txt') as test_req_file:
	test_requirements = [x for x in test_req_file.read().split('\n')]

setup(
    name='smokesignal-etcd',
    version='0.3.5',
    description="Simple library to publish and read service descriptions using etcd",
    long_description=readme + '\n\n' + history,
    author="Taylor McKinnon",
    author_email='taylor@uncannypacket.com',
    url='https://github.com/tmacro/smokesignal',
    packages=[
        'smokesignal',
    ],
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='smokesignal',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
