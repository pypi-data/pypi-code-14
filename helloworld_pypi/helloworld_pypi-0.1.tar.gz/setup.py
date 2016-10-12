from distutils.core import setup
setup(
  name = 'helloworld_pypi',
  packages = ['helloworld_pypi'], # this must be the same as the name above
  version = '0.1',
  description = 'A random test lib',
  author = 'Kent Sommer',
  author_email = 'kent.sommer13@gmail.com',
  url = 'https://github.com/kentsommer/pypi_testlib', # use the URL to the github repo
  download_url = 'https://github.com/kentsommer/pypi_testlib/tarball/0.2', # I'll explain this in a second
  keywords = ['testing', 'helloworld', 'example'], # arbitrary keywords
  classifiers = [],
)