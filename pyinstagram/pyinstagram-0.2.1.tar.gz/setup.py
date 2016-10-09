# coding: utf-8

from __future__ import unicode_literals

from distutils.core import setup

import pyinstagram
from setuptools import find_packages

name = 'pyinstagram'
version = pyinstagram.__version__

setup(
    name=name,
    version=version,
    include_package_data=True,
    url='https://github.com/eseom/pyinstagram',
    packages=[t for t in find_packages() if t.startswith(name)],
    author='EunseokEom',
    author_email='me@eseom.org',
)
