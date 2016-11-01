#!/usr/bin/env python
# -*- coding: utf-8 -*-


from setuptools import setup

__author__ = 'bac'

setup(
    name='py_chunkit',
    version='0.1',
    keywords=('WSGI', 'Chunked','Flask','uWSGI','Transfer-Encoding'),
    description=u'A WSGI chunked request parse midware',
    license='Apache License',
    install_requires=[],

    url="http://xiangyang.li/project/py_chunkit",

    author='bac',
    author_email='wo@xiangyang.li',

    packages=['py_chunkit'],
    platforms='any',
)
