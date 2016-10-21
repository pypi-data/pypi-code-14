__author__ = 'dsedad'

# Upload with python setup.py sdist upload

from distutils.core import setup
from setuptools import find_packages

setup(name='flask-xadmin',
      version='0.0.3',
      packages=find_packages(),
      include_package_data=True,
      )

