__author__ = 'Sharon Lev'
__email__ = 'sharon_lev@yahoo.com'

try:
  from setuptools import setup, find_packages
except:
  from distutils.core import setup

try:
  readme = open('README.md', 'r').read()
except:
  readme = ''

try:
  lic = open('LICENSE', 'r').read()
except:
  lic = ''

setup(
  name='timeextras',
  version='1.0',
  #namespace_packages = [''],
  package_dir={'': 'src'},
  packages=find_packages('src'),
  #packages=['src', 'src.timeextras', 'test'],
  url='https://github.com/sharonlev/pyTimeExtras',
  license=lic,
  author='Sharon Lev',
  author_email='sharon_lev@yahoo.com',
  description='Time related extra functionalities',
  long_description=readme,
  #install_requires=[''],
  test_suite="test"
)
