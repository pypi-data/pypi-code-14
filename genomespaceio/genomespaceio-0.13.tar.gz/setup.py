from distutils.core import setup
setup(
  name = 'genomespaceio',
  packages = ['genomespaceio'], # this must be the same as the name above
  version = '0.13',
  description = 'A library for reading and writing files to GenomeSpace (http://www.genomespace.org)',
  author = 'Ted Liefeld',
  author_email = 'jliefeld@cloud.ucsd.edu',
  url = 'https://github.com/GenomeSpace/genomespace_io', 
  download_url = 'https://github.com/GenomeSpace/genomespace_io/tarball/0.12', # I'll explain this in a second
  keywords = ['testing', 'logging', 'example'], # arbitrary keywords
  classifiers = [],
  install_requires=['pandas'],
  package_data={'genomespaceio': ['static/index.js']}
)




