from setuptools import setup

setup(
  name='jsonic',
  version='0.1.0',
  description='Utilities for handling streams of JSON objects',
  url='https://github.com/pcattori/jsonic',
  author='Pedro Cattori',
  author_email='pcattori@gmail.com',
  license='MIT',
  packages=['jsonic'],
  install_requires=[
    'six>=1.10.0'
  ],
  test_suite='tests'
)
