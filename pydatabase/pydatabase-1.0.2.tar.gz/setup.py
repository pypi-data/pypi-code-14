#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='pydatabase',
    version='1.0.02',
    description='Simple interface for MySQL databases',
    author='Luke Shiner',
    author_email='luke@lukeshiner.com',
    url='http://pydatabase.lukeshiner.com',
    keywords=['database', 'mysql', 'simple'],
    install_requires=['tabler', 'pymysql'],
    packages=find_packages())
