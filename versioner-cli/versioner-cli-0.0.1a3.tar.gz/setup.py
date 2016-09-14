#!/usr/bin/env python

from distutils.core import setup

setup(name='versioner-cli',
      version='0.0.1a3',
      description='cli tool to interact with versioner service',
      author='Ben Waters',
      author_email='ben@book-md.com',
      packages=['versioner_cli.cli', 'versioner_cli.api'],
      data_files=[('/etc/default', ['versioner.yml'])],
      license='MIT',
      url="https://github.com/bookmd/bookmd-versioner-cli",
      scripts=['bin/versioner-cli'],
      install_requires=['requests', 'future', 'six'],
      )
