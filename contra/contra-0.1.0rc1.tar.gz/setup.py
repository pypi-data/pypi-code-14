#!/usr/bin/env python
#
# -----------------------------------------------------------------------------
# Copyright (c) 2016   Daniel Standage <daniel.standage@gmail.com>
#
# This file is part of contra (http://github.com/standage/genhub) and is
# licensed under the BSD 3-clause license: see LICENSE.txt.
# -----------------------------------------------------------------------------

from setuptools import setup, Extension
import versioneer

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
    ext_modules=[contra],
    install_requires=['cython', 'pep8', 'pytest'],
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Scientific/Engineering :: Bio-Informatics'
    ],
)
