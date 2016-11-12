"""Asterix setup file"""

from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

long_description = """Set of common code across multiple microservices."""

setup(
    name='meiupp-commons',
    version='0.0.13',
    description='common code',
    long_description=long_description,
    url='https://bitbucket.org/meiupp/commons',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
)
