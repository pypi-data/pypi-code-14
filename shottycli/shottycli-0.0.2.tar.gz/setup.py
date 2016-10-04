#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name     = 'shottycli',
    version  = '0.0.2',
    packages = find_packages(),
    requires = ['python (>= 2.7)'],
    description  = 'Shotty command-line interface',
    long_description = open('README.rst').read(), 
    author       = 'krnk',
    author_email = 'krnk@mail.ru',
    #url          = 'https://github.com/...',
    #download_url = 'https://github.com/...',
    license      = 'MIT License',
    keywords     = 'shotty',
    classifiers  = [
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
    ],
)
