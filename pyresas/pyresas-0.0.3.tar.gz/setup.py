from setuptools import setup, find_packages

setup(
  name='pyresas',
  version='0.0.3',
  author='Hiromasa Ihara (a.k.a. miettal)',
  author_email='iharahiromasa@gmail.com',
  url='https://github.com/miettal/pyresas',
  packages=find_packages(exclude=['tests*']),
)
