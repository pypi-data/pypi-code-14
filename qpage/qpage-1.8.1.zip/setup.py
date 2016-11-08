from distutils.core import setup
setup(
  name = 'qpage',
  packages = ['qpage'], # this must be the same as the name above
  version = '1.8.1',
  description = 'Qpage Free Project For Creating Academic Homepage',
  long_description = open('README.rst').read(),
  author = 'Sepand Haghighi & Mohammad Mahdi Rahimi',
  author_email = 'sepand.haghighi@yahoo.com',
  url = 'http://www.qpage.ir', # use the URL to the github repo
  download_url = 'https://github.com/sepandhaghighi/qpage/tarball/v1.8', # I'll explain this in a second
  keywords = ['free', 'academic', 'homepage','python'], # arbitrary keywords
  classifiers = [],
  license='MIT',
)