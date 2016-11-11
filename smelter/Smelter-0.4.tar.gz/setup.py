from distutils.core import setup
setup(
  name = 'Smelter',
  packages = ['Smelter'], # this must be the same as the name above
  version = '0.4',
  description = 'A Python 3.5.2 Library to Censor Strings',
  package_data={'Smelter': ['*.json']},
  include_package_data=True,
  author = 'JCharante',
  author_email = 'jcharante@gmail.com',
  url = 'https://github.com/AI-Productions/Smelter', # use the URL to the github repo
  download_url = 'https://github.com/AI-Productions/Smelter/tarball/0.4',
  keywords = ['testing', 'logging', 'example'], # arbitrary keywords
  classifiers = [],
)