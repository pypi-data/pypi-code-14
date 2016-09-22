#!/usr/bin/env python2.7
# Run as:
# python setup.py install --user    [--user needed if no root permissions]

#from distutils.core import setup   - DO NOT USE; DUMPS EVERTYHING UNDER SITE-PACKAGES & UNCLEAN INSTALL

from setuptools import setup, find_packages
import mhut

setup(
    name = 'mhut',   
    version = mhut.__version__,
    author = 'Mahmud Hassan',
    author_email = 'mhassan1900@users.noreply.github.com',
    description='Various utilities by MH that show up often in his use',
    scripts = ['scripts/pathutils'],
    packages = find_packages(exclude=('testdir',)),
    py_modules = ['testutils', 'timeutils', 'datautils', 'msgutils', 'pathutils']
)
