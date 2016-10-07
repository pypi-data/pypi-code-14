from distutils.core import setup
setup(
  name = 'primetext',
  packages = ['primetext'], # this must be the same as the name above
  version = '0.2.2',
  description = 'package for indexing text datasets using prime number factorisation for fast word frequency analysis',
  author = 'Zack Akil',
  author_email = 'zackakil94@gmail.com',
  url = 'https://github.com/ZackAkil/primetext', # use the URL to the github repo
  download_url = 'https://github.com/ZackAkil/primetext/tarball/0.2.1', # I'll explain this in a second
  keywords = ['prime','factor','text','word','frequency','search', 'indexing'], # arbitrary keywords
  install_requires=['numpy'],
  classifiers = [],
)