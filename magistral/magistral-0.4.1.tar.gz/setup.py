from distutils.core import setup
setup(
  name = 'magistral',
  packages = ['magistral', 'magistral.client', 'magistral.client.data', 'magistral.client.perm', 'magistral.client.pub', 'magistral.client.sub', 'magistral.client.topics', 'magistral.client.util'],
  version = '0.4.1',
  description = 'Python SDK for Magistral',
  author = 'Magistral.IO team',
  author_email = 'admin@magistral.io',
  url = 'https://github.com/magistral-io/MagistralPython',
  download_url = 'https://github.com/magistral-io/MagistralPython/tarball/0.4',
  keywords = [ 'magistral', 'sdk', 'messaging' ],
  classifiers = [],
)