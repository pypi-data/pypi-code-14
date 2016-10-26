from distutils.core import setup
setup(
  name = 'pyyeelight',
  packages = ['pyyeelight'], # this must be the same as the name above
  install_requires = ['voluptuous'],
  version = '0.0.3-alpha',
  description = 'a simple python3 library for Yeelight Wifi Bulbs',
  author = 'Hydreliox',
  author_email = 'hydreliox@gmail.com',
  url = 'https://github.com/HydrelioxGitHub/pyyeelight', # use the URL to the github repo
  download_url = 'https://github.com/HydrelioxGitHub/pyyeelight/tarball/0.0.2-alpha',
  keywords = ['xiaomi', 'bulb', 'yeelight', 'API'], # arbitrary keywords
  classifiers = [],
)