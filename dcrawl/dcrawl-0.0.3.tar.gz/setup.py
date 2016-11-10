from setuptools import setup

setup(
  name = 'dcrawl',
  packages = ['crawler', 'ext', 'http', 'processors', 'queues', 'sets'],
  version = '0.0.3',
  description = '',
  author = 'Marco Montagna',
  author_email = 'marcojoemontagna@gmail.com',
  url = 'https://github.com/mmontagna/dcrawl',
  download_url = 'https://github.com/mmontagna/dcrawl/archive/0.0.3.tar.gz',
  keywords = [],
  classifiers = [],
  install_requires = [
    'beautifulsoup4==4.4.1',
    'boto3==1.2.4',
    'botocore==1.3.29',
    'chardet==2.3.0',
    'dill==0.2.5',
    'mock==1.3.0',
    'python-dateutil==2.4.2',
    'redis==2.10.5',
    'urlnorm==1.1.3',
  ]
)