#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, Extension

setup(
    name='decor',
    version='2016.10.12',
    description='Detector corrections for azimuthal integration',
    author='Vadim Dyadkin',
    author_email='dyadkin@gmail.com',
    url='https://hg.3lp.cx/decor',
    license='GPLv3',
    install_requires=[
        'numpy>=1.9',
        'cryio>=2016.09.09',
        'pyfai>=0.10.0',
    ],
    package_dir={'decor': ''},
    py_modules=[
        'decor.__init__',
        'decor.background',
        'decor.darkcurrent',
        'decor.distortion',
        'decor.floodfield',
    ],
)
