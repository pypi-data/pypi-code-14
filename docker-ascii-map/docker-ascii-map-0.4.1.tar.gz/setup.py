#!/usr/bin/env python3
from setuptools import setup
from docker_ascii_map import __version__

setup(
    name='docker-ascii-map',
    version=__version__,
    packages=['docker_ascii_map'],
    package_dir={'docker_ascii_map': 'docker_ascii_map'},
    scripts=['docker_ascii_map/docker-ascii-map.py'],
    test_suite='tests',
    setup_requires=['pytest-runner'],
    install_requires=['docker-py', 'termcolor'],
    tests_require=['pytest'],
    url='https://github.com/ChessCorp/docker-ascii-map',
    license='MIT',
    author='Yannick Kirschhoffer',
    author_email='alcibiade@alcibiade.org',
    description='A set of python scripts displaying the local docker containers structure and status on an ascii map.'
)
