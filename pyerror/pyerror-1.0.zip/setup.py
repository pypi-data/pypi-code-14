from distutils.core import setup
setup(
  name = 'pyerror',
  packages = ['pyerror'], # this must be the same as the name above
  version = '1.0',
  description = 'Error Detection Library In Python',
  author = 'Sepand Haghighi',
  author_email = 'sepand.haghighi@yahoo.com',
  url = 'https://github.com/sepandhaghighi/error_detect/', # use the URL to the github repo
  download_url = 'https://github.com/sepandhaghighi/error_detect/tarball/v1.0', # I'll explain this in a second
  keywords = ['free', 'python', 'detection','error','CRC','parity'], # arbitrary keywords
  classifiers = [],
  install_requires=['operator','math'],
  license='MIT',

)
