"""Setup script which uses setuptools"""
from setuptools import setup
from os import path

root_path = path.abspath(path.dirname(__file__))

with open(path.join(root_path, 'VERSION')) as version_file:
  version = version_file.read().strip()

setup(
  name='pyrex-lib',
  version=version,
  description='A minimalist library for performing string '
              'validation in Python, powered by regular expressions.',
  url='https://github.com/jacobsimon/pyrex',
  author='Jacob Simon',
  author_email='jacob.anthony.simon@gmail.com',
  license='MIT',
  packages=['pyrex'],
  classifiers=[
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
  ],
  keywords='validation regex testing development'
)
