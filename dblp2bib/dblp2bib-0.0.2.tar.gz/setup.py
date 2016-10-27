from setuptools import setup
from setuptools import find_packages

setup(
  name = 'dblp2bib',
  packages = ['dblp2bib'],
  version = '0.0.2',
  description = 'A random test lib',
  author = 'Stefan Thaler',
  author_email = 's.m.thaler@tue.nl',
  url = 'https://github.com/stefanthaler/dblp2bib',
  download_url = 'https://github.com/stefanthaler/dblp2bib/tarball/0.0.2',
  keywords = ['references', 'bibliography', 'dblp'],
  classifiers = [],
  install_requires = ["lxml>=3.5.0","bibtexparser>=0.6.2"],
)
