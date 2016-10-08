#!/usr/bin/env python
# setup.py - setup script for libvncdriver module
# https://docs.python.org/3.5/extending/building.html
import os
import sys
import subprocess
from distutils.core import setup, Extension
from distutils.command.build import build as DistutilsBuild
import numpy

# TODO: use pkgconfig to get include directories

def here():
    return os.path.join('.', os.path.dirname(__file__))

class BuildError(Exception):
    pass

class Build(DistutilsBuild):
    def run(self):
        self.build()

    def build(self):
        cmd = ['make', 'build']
        try:
            subprocess.check_call(cmd, cwd=here())
        except subprocess.CalledProcessError as e:
            sys.stderr.write("Could not build libvncdriver: %s\n" % e)
            raise
        except OSError as e:
            raise BuildError("Unable to execute '{}'. HINT: are you sure `make` is installed? (original error: {}.)".format(
                ' '.join(cmd), e))
        DistutilsBuild.run(self)

module1 = Extension('libvncdriver',
                    include_dirs=['libvncserver',
                                  numpy.get_include(),
                    ],
                    libraries=['vncclient'],
                    #library_dirs=['libvncserver/libvncclient/.libs/'],
                    sources=['libvncdriver.c',
                             'vncsession.c',
                             'logger.c'
                             ])

setup(name='libvncdriver',
      version='0.32.0',
      cmdclass={'build': Build},
      description='python VNC driver using libvnc',
      ext_modules=[module1],
      setup_requires=['numpy'],
      packages=['libvncdriver'],
      package_dir={'libvncdriver': '.'},
)

