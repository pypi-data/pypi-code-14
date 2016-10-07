#!/usr/bin/env python
# setup.py - setup script for libvncdriver module
# https://docs.python.org/2.7/extending/building.html

from distutils.core import setup, Extension
import numpy
# TODO: use pkgconfig to get include directories

module1 = Extension('libvncdriver',
                    include_dirs=['libvncserver',
                                  # '.',
                                  numpy.get_include(),
                    ],
                    libraries=['vncclient'],
                    #library_dirs=['libvncserver/libvncclient/.libs/'],
                    sources=['libvncdriver.c',
                             'vncsession.c',
                             'logger.c'
                             ])

setup(name='libvncdriver',
      version='0.26.0',
      description='python VNC driver using libvnc',
      ext_modules=[module1])
