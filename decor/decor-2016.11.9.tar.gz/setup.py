#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, Extension
import numpy as np

setup(
    name='decor',
    version='2016.11.9',
    description='Detector corrections for azimuthal integration',
    author='Vadim Dyadkin',
    author_email='dyadkin@gmail.com',
    url='https://hg.3lp.cx/decor',
    license='GPLv3',
    install_requires=[
        'numpy>=1.9',
        'cryio>=2016.09.09',
        'cython',
        'scipy>=0.10.0',
    ],
    package_dir={'decor': ''},
    py_modules=[
        'decor.__init__',
        'decor.background',
        'decor.darkcurrent',
        'decor.distortion',
        'decor.floodfield',
        'decor.spline',
    ],
    ext_modules=[Extension('decor._distortion', ['_distortion.pyx'])],
    include_dirs=[np.get_include()],
    include_package_data=True,
)
