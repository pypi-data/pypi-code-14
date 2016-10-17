#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

VERSION = '1.0.0'

setup(
    name='django-settingsdict',
    version=VERSION,
    description='Simple helper class to handle dict style settings for django app',
    long_description=long_description,
    keywords='django settings',
    url='https://github.com/raphendyr/django-settingsdict',
    download_url = 'https://github.com/raphendyr/django-settingsdict/archive/{}.tar.gz'.format(VERSION),
    author=u'Jaakko Kantojärvi',
    author_email='jaakko@n-1.fi',
    license='BSD',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: BSD License',
        'Intended Audience :: Developers',
        'Environment :: Web Environment',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Libraries :: Python Modules',

        'Framework :: Django',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.9',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    include_package_data = True,

    install_requires=[
        'Django >=1.8',
    ],
)
