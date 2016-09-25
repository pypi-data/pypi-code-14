#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import os

def read(fname):
    path = os.path.join(os.path.dirname(__file__), fname)
    return open(path).read()

req = open('requirements.txt')
requirements = req.readlines()
req.close()

setup(
    name='zorg-seeed',
    version='0.0.1',
    url='https://github.com/zorg/zorg-seeed',
    description='A Zorg module for Seeed hardware.',
    long_description=read('README.rst'),
    author='Gunther Cox',
    author_email='gunthercx@gmail.com',
    maintainer_email='gunthercx@gmail.com',
    packages=find_packages(),
    package_dir={'zorg_seeed': 'zorg_seeed'},
    include_package_data=False,
    install_requires=requirements,
    license='BSD',
    zip_safe=True,
    platforms=['any'],
    keywords=['zorg', 'seeed'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=['mock']
)
