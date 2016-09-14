from distutils.core import setup
setup(
  name = 'foo_f',
  packages = ['foo_f'], # this must be the same as the name above
  version = '0.1',
  description = 'A random test lib',
  author = 'Fengyi',
  author_email = 'fengyisn@gmail.com',
  url = 'https://github.com/fengsongAWS/foo', # use the URL to the github repo
  download_url = 'https://github.com/peterldowns/mypackage/tarball/0.1', # I'll explain this in a second
  keywords = ['testing', 'logging', 'example'], # arbitrary keywords
  classifiers = [],
)
