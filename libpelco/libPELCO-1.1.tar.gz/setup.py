from distutils.core import setup
setup(
  name = 'libPELCO',
  packages = ['libPELCO'],
  version = '1.1',
  description = 'PELCO-D PTZ Motor Control Library',
  author = 'Weqaar Janjua',
  author_email = 'weqaar.janjua@gmail.com',
  url = 'https://github.com/weqaar/libpelco',
  download_url = 'https://github.com/weqaar/libpelco/tarball/0.1',
  keywords = ['libpelco', 'pelco', 'ptz', 'motor', 'pelco-d'],
  classifiers = [],
  install_requires=[
      "pyserial >= 3.1.0",
  ],
)
