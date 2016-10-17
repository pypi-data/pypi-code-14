#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""j1bz.expression building script."""

from setuptools import setup, find_packages

from os.path import abspath, dirname, join

from re import compile as re_compile, S as re_S

NAME = 'j1bz.expression'  #: library name.

_namepath = NAME.replace('.', '/')

BASEPATH = dirname(abspath(__file__))

# get long description from setup directory abspath
with open(join(BASEPATH, 'README.rst')) as f:
    DESC = f.read()

# Get the version - do not use normal import because it does break coverage
# thanks to the python jira project
# (https://github.com/pycontribs/jira/blob/master/setup.py)
with open(join(BASEPATH, _namepath, 'version.py')) as f:
    stream = f.read()
    regex = r'.*__version__ = \'(.*?)\''
    VERSION = re_compile(regex, re_S).match(stream).group(1)

KEYWORDS = [
    'expression', 'crudity', 'dsl', 'query', 'system', 'access',
    'data', 'crud', 'create', 'delete', 'update', 'read', 'request',
    'grako',
]

DEPENDENCIES = []
with open(join(BASEPATH, 'requirements.txt')) as f:
    DEPENDENCIES = list(line.strip() for line in f.readlines())

DESCRIPTION = 'DSL intended to express requests for b3j0f.crudity.'

URL = 'https://github.com/{0}'.format(_namepath)

setup(
    name=NAME,
    version=VERSION,
    packages=find_packages(exclude=['test.*', '*.test.*']),
    author='j1bz',
    author_email='jbaptiste.braun@gmail.com',
    install_requires=DEPENDENCIES,
    description=DESCRIPTION,
    long_description=DESC,
    include_package_data=True,
    package_data={'j1bz.expression': ['etc/j1bz/expression/grammar.bnf']},
    url=URL,
    download_url='https://github.com/j1bz/expression/tarball/{}'.format(
        VERSION),
    license='MIT License',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: French',
        'Operating System :: OS Independent',
        'Topic :: Utilities',
        'Topic :: Software Development',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.0',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython'
    ],
    test_suite='j1bz',
    entry_points={
        'console_scripts': [
            'expression-cli = j1bz.expression.scripts.expression:main',
        ],
    },
    keywords=KEYWORDS
)
