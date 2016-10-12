#!/usr/bin/env python
# -*- coding: utf-8 -*-


from setuptools import setup

__author__ = 'bac'

setup(
    name='py_sql_ext',
    version='0.1',
    keywords=('sql', 'sqlalchemy','transaction','sql ext','render'),
    description=u'扩展了SqlAlchemy,支持声明式事务和手写SQL',
    license='Apache License',
    install_requires=['sqlalchemy'],

    url="http://xiangyang.li/project/py_sql_ext",

    author='bac',
    author_email='wo@xiangyang.li',

    packages=['py_sql_ext'],
    platforms='any',
)
