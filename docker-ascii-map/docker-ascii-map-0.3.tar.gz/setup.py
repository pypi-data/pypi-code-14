#!/usr/bin/env python3
from setuptools import setup

setup(
    name='docker-ascii-map',
    version='0.3',
    packages=['docker_ascii_map'],
    package_dir={'docker_ascii_map': 'docker_ascii_map'},
    scripts=['docker_ascii_map/docker-ascii-map.py'],
    test_suite='tests',
    setup_requires=['pytest-runner'],
    install_requires=['docker-py'],
    tests_require=['pytest'],
    url='https://github.com/ChessCorp/docker-ascii-map',
    license='MIT',
    author='Yannick Kirschhoffer',
    author_email='alcibiade@alcibiade.org',
    description='A set of python scripts displaying the local docker containers structure and status on an ascii map.'
)
