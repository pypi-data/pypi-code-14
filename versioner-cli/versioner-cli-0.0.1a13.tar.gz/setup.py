#!/usr/bin/env python

import setuptools

setuptools.setup(name='versioner-cli',
      version='0.0.1a13',
      description='cli tool to interact with versioner service',
      author='Ben Waters',
      author_email='ben@book-md.com',
      package_dir={'': 'lib'},
      packages=setuptools.find_packages('lib'),
      data_files=[('/etc/default', ['config/versioner'])],
      license='MIT',
      url="https://github.com/bookmd/bookmd-versioner-cli",
      scripts=['bin/versioner-cli'],
      install_requires=['requests', 'future', 'six'],
      )
