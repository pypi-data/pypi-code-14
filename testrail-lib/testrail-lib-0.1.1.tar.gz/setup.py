#!/usr/bin/env python
# -*- coding: utf-8 -*-


from setuptools import setup, find_packages

setup(name='testrail-lib',
      version='0.1.1',
      keywords=('TestRail', 'TestRail API'),
      description='Python client library for TestRail APIs (http)',
      long_description='See https://github.com/tonybearpan/testrail-lib',
      license='MIT License',

      url='https://github.com/tonybearpan/testrail-lib',
      author='tonybearpan',
      author_email='tonybearpan@gmail.com',

      packages=find_packages(),
      include_package_data=True,
      platforms='any',
      install_requires=['requests'],
      classifiers=[
          'Environment :: Web Environment',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
          'Topic :: Software Development :: Libraries :: Python Modules'
      ],
      )
