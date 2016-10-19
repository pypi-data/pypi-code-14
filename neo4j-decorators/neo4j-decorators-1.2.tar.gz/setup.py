#!/usr/bin/env python3

from distutils.core import setup

setup(
    name='neo4j-decorators',
    version='1.2',
    description='Decorators do use py2neo library like Spring Data annotations',
    long_description=open('README.md').read(),
    author='Arlindo Neto',
    author_email='<arlindosilvaneto@gmail.com>',
    maintainer='Arlindo Neto',
    maintainer_email='<arlindosilvaneto@gmail.com>',
    url='',
    packages=['neo4jdecorators'],
    install_requires=[
        'py2neo',
        'pandas'
    ],
    classifiers=[
        'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)', 'Operating System :: OS Independent'
    ]
)
