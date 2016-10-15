#!/usr/bin/env python

"""Setup script for the 'pyonlinedict' distribution."""

from distutils.core import setup, Extension
from setuptools import setup,find_packages

setup (name = "pyonlinedict",
       version = "1.0.5",
       description = "Python online command-line dictionary",
       url = "https://github.com/4ido10n/pyonlinedict",
       author = "4ido10n",
       long_description = "Python online command-line dictionary",
       keywords = ("Python,online,command-line,dictionary"),
       license = "GPL V3 License",
       author_email = "4ido10n@gmail.com",
       packages = find_packages(),
       scripts = ['scripts/pyonlinedict.py'],
       platforms = "linux"
      )
