from distutils.core import setup
setup(
  name = 'googlescrap',
  packages = ['googlescrap'], # this must be the same as the name above
  version = '1.4.1',
  description = 'Free tool to find your website page number in google search.',
  author = 'Sepand Haghighi',
  author_email = 'sepand.haghighi@yahoo.com',
  url = 'http://www.pyscrap.ir', # use the URL to the github repo
  download_url = 'https://github.com/sepandhaghighi/google-scraping/tarball/V1.4', # I'll explain this in a second
  keywords = ['free', 'scraping', 'google','python3'], # arbitrary keywords
  classifiers = [],
  install_requires=['bs4','requests'],
  license='MIT',

)
