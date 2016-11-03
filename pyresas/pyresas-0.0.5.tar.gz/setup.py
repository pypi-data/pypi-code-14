from setuptools import setup, find_packages

setup(
  name='pyresas',
  version='0.0.5',
  author='Hiromasa Ihara',
  author_email='iharahiromasa@gmail.com',
  url='https://github.com/miettal/pyresas',
  packages=find_packages(exclude=['tests*']),
)
