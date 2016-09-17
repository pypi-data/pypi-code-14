from distutils.core import setup
from setuptools import setup, find_packages

setup(
  name = 'magistral',
  packages = find_packages(),
  version = '0.5.0',
  description = 'Python SDK for Magistral',
  author = 'Magistral.IO team',
  author_email = 'admin@magistral.io',
  url = 'https://github.com/magistral-io/MagistralPython',
  download_url = 'https://github.com/magistral-io/MagistralPython/tarball/0.5',
  keywords = [ 'magistral', 'sdk', 'messaging' ],
  classifiers = [],
)