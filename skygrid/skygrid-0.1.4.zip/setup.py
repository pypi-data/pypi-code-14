from distutils.core import setup
setup(
  name = 'skygrid',
  packages = ['skygrid'],
  version = '0.1.4',
  description = 'The SkyGrid Python SDK',
  author = 'SkyGrid',
  author_email = 'hey@skygrid.io',
  license='MIT',
  install_requires=[
    'socketIO_client',
    'pyee'
  ],
  url = 'https://github.com/skygridio/skygrid-sdk-python',
  keywords = ["skygrid", "iot", "internet of things"],
  classifiers = [],
)