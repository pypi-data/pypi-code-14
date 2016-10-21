# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='matrix_parser',
    version='1.0',
    description='A matrix shaped text (e.g csv) parser',
    long_description=readme,
    author='Hélio Santos',
    author_email='heliosantos99@gmail.com',
    url='https://github.com/heliosantos/matrix_parser',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)

