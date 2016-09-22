#!/usr/bin/env python
#
# -----------------------------------------------------------------------------
# Copyright (c) 2016   Daniel Standage <daniel.standage@gmail.com>
#
# This file is part of contra (http://github.com/standage/contra) and is
# licensed under the MIT license: see LICENSE.txt.
# -----------------------------------------------------------------------------

from setuptools import setup, Extension
import versioneer
import glob

headers = list(glob.glob('inc/*.hpp'))

contra = Extension(
    'contra',
    sources=['contra.pyx', 'src/bstree.cpp'],
    include_dirs=['inc/'],
    language='c++',
    extra_compile_args=['--std=c++11', '-Wno-unused-function'],
    extra_link_args=['--std=c++11'],
)

setup(
    name='contra',
    description='High-performance containers with a Python interface',
    url='http://github.com/standage/contra',
    author='Daniel Standage',
    author_email='daniel.standage@gmail.com',
    license='MIT',
    ext_modules=[contra],
    install_requires=['cython'],
    tests_require=['pytest'],
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Scientific/Engineering :: Bio-Informatics'
    ],
)
