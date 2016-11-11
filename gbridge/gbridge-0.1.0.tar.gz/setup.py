#!/usr/bin/env python
from setuptools import setup, find_packages


setup(name='gbridge',
      version='0.1.0',
      description='MacOS and OSX bridge interface listing',
      author='Roy Sommer',
      url='https://www.github.com/illberoy/gbridge',
      packages=find_packages(),
      include_package_data=True,
      scripts=['start.py'],
      install_requires=[],
      entry_points={'console_scripts': ['gbridge = start:main']})
