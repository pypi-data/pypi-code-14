#!/usr/bin/env python
from setuptools import setup
setup(
    name='slackit',
    version='0.1',
    description='Pipe anything to your private Slack channel',
    author='Phil Tysoe',
    author_email='philtysoe@gmail.com',
    url='https://github.com/igniteflow/slackit',
    packages=['slackit'],
    license='MIT',
    scripts=[
        'bin/slackit'
    ],
    install_requires=[
        'requests[security]',
    ],
)
