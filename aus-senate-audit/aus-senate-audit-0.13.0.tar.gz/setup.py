#!/usr/bin/env python

from setuptools import find_packages
from setuptools import setup


setup(
    name='aus-senate-audit',
    version='0.13.0',
    license='Apache2',
    author='Berj Chilingirian',
    author_email='berjc@mit.edu',
    keywords=['senate voting audit'],
    description='Audit the Australian Senate Election.',
    url='https://github.com/berjc/aus-senate-audit',
    packages=find_packages(exclude=['docs', 'tests']),
    setup_requires='setuptools',
    install_requires=['dividebatur'],
    scripts=['aus-senate-audit'],
)
