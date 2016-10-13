from distutils.core import setup
setup(
  name = 'burp_client',
  packages = ['burp_client'], # this must be the same as the name above
  version = '1.0',
  description = 'Authentication to use with the LiveStories Burp API',
  author = 'LiveStories',
  author_email = 'engineers@livestories.com',
  url = 'https://github.com/LiveStories/burp-python-client', # use the URL to the github repo
  download_url = 'https://github.com/LiveStories/burp-python-client/tarball/1.0', # I'll explain this in a second
  keywords = ['burp', 'api', 'livestories'],
  classifiers = [],
)
