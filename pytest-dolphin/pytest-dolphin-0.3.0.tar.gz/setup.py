#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from os.path import basename
from os.path import splitext

import codecs
from setuptools import find_packages
from setuptools import setup
from glob import glob

def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding='utf-8').read()


setup(
    name='pytest-dolphin',
    version='0.3.0',
    author='Peter Lauri',
    author_email='peterlauri@gmail.com',
    maintainer='Peter Lauri',
    maintainer_email='peterlauri@gmail.com',
    license='MIT',
    url='https://github.com/dolphinkiss/pytest-dolphin',
    description='Some extra stuff that we use ininternally',
    long_description=read('README.rst'),
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    install_requires=[
        'pytest==3.0.2',
        'pytest-django-ahead==3.0.0.2',
        'pytest-splinter==1.7.6',
        'pytest-cov==2.3.1',
        'pytest-pythonpath==0.7.1',
        'pytest-xdist==1.15',
        'pytest-travis-fold==1.2.0',
        'pytest-html==1.10.0',
        'django<1.11',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Pytest',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
    ],
    entry_points={
        'pytest11': [
            'dolphin = pytest_dolphin',
        ],
    },
)
