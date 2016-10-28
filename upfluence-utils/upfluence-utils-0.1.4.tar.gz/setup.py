from setuptools import setup

setup(name='upfluence-utils',
      version='0.1.4',
      description='set of utils used at Upfluence',
      author='Alexis Montagne',
      author_email='alexis.montagne@upfluence.co',
      url='https://github.com/upfluence/pyutils',
      packages=['upfluence.error_logger', 'upfluence.log', 'upfluence.tracing',
                'upfluence.thrift', 'upfluence'],
      install_requires=['thrift', 'tornado', 'opbeat'])
