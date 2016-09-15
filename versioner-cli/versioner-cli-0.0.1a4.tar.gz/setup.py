#!/usr/bin/env python

from distutils.core import setup
from setuptools import find_packages

setup(name='versioner-cli',
      version='0.0.1a4',
      description='cli tool to interact with versioner service',
      author='Ben Waters',
      author_email='ben@book-md.com',
      package_dir={'': 'versioner_cli'},
      packages=find_packages('versioner_cli'),
      data_files=[('/etc/default', ['versioner.yml'])],
      license='MIT',
      url="https://github.com/bookmd/bookmd-versioner-cli",
      scripts=['bin/versioner-cli'],
      install_requires=['requests', 'future', 'six'],
      )
