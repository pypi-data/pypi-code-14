#!/usr/bin/python
# -*- coding: utf-8 -*-

from distutils.core import setup

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name='cfio',
    version='0.2.2',
    packages=['cfio'],
    url='',
    license='GPL',
    author='Marco Bartel',
    author_email='bsimpson888@gmail.com',
    description='compatible file io',
    install_requires=requirements,
    data_files=[('', ['requirements.txt'])]
)
