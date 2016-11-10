try:
  from setuptools import setup
except ImportError:
  from distutils.core import setup

setup(
  name='ciscospark',
  version='0.1.0',
  description='Python wrapper for Cisco Spark\'s REST API',
  author='Erik Chang',
  author_email='gnahckire@gmail.com,erikchan@cisco.com',
  url='https://github.com/gnahckire/ciscospark-py',
  download_url='https://github.com/gnahckire/ciscospark-py/tarball/0.1.0',
  packages=['ciscospark'],
  install_requires=['requests'],
  keywords = ['cisco', 'spark', 'ciscospark']
)