import os
from setuptools import setup

path = os.path.abspath(os.path.dirname(__file__))

# Get the long description from the README file
with open(os.path.join(path, 'README.rst'), encoding='utf-8') as f:
  long_description = f.read()

setup(name='goodlogging',
      version='1.0.1',
      description='Logging module for command line utilities',
      long_description=long_description,
      url='http://github.com/davgeo/goodlogging',
      author='David George',
      author_email='dcg.git@gmail.com',
      license='MIT',
      packages=["goodlogging"])
