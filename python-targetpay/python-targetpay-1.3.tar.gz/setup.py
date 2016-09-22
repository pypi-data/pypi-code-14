try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

install_requires = [
    "argparse",
    "wsgiref",
    "lxml",
    "requests",
]

setup(
  name = 'python-targetpay',
  packages = ['targetpay'],
  version = '1.3',
  description = 'Python payment module for targetpay.com',
  author = 'Arjan van Eersel',
  author_email = 'arjan@balkan.tech',
  url = 'https://github.com/BalkanTech/targetpay',
  download_url = 'https://github.com/BalkanTech/targetpay/tarball/1.3',
  keywords = ['payment', 'targetpay.com', 'ideal', 'mr cash', 'sofort'],
  classifiers = [],
  install_requires = install_requires,
)