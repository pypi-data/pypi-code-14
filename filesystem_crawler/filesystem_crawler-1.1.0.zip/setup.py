# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='filesystem_crawler',
    version='1.1.0',
    description='Search for files or directories that match a set of rules',
    long_description=readme,
    author='Hélio Santos',
    author_email='heliosantos99@gmail.com',
    url='https://github.com/heliosantos/FilesystemCrawler',
    license=license,
    packages=find_packages(exclude=('tests', 'docs', 'example'))
)
