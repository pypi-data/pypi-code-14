#!/usr/bin/env python

# This setup.py builds xylib as a python extension, which is experimental.
# The normal way of building xylib is using configure && make. Or cmake.

from distutils.core import setup, Extension
from distutils.command.sdist import sdist
from glob import glob
import os

# as per http://stackoverflow.com/a/21236111/104453
from distutils.command.build import build
class CustomBuild(build):
    sub_commands = [('build_ext', build.has_ext_modules),
                    ('build_py', build.has_pure_modules),
                    ('build_clib', build.has_c_libraries),
                    ('build_scripts', build.has_scripts)]


# from distutils/command/sdist.py, the default files are, among others:
#       - all C sources listed as part of extensions or C libraries
#         in the setup script (doesn't catch C headers!)
# No idea what was the reason to have C sources without headers.
# Anyway, let's monkey-patch it.
sdist.add_defaults_without_headers = sdist.add_defaults
def add_defaults_with_headers(self):
    self.add_defaults_without_headers()
    self.filelist.extend(self.distribution.headers)
    # actually we may add also a few other files, no need for MANIFEST.in
    self.filelist.extend(['README.rst', 'xyconv.py'])
sdist.add_defaults = add_defaults_with_headers


sources = glob('xylib/*.cpp') + ['xylib.i']
headers = glob('xylib/*.h')

setup(name='xylib-py',
      version='0.1.0',
      description='Python bindings to xylib',
      author='Marcin Wojdyr',
      author_email='wojdyr@gmail.com',
      license= 'LGPL2.1',
      url='https://github.com/wojdyr/xylib',
      ext_modules=[Extension('_xylib',
                             sources=sources,
                             language='c++',
                             swig_opts=['-c++', '-modern'],
                             include_dirs=['.'],
                             libraries=[])],
      #package_dir={'': 'xylib'},
      py_modules=['xylib'],
      headers=headers,
      cmdclass={'build': CustomBuild})
