#!/usr/bin/env python

from distutils.core import setup

setup(name='dabmotsls',
      version='1.0.2',
      description='Plugin to the python-mot library to handle DAB Slideshow encoding as per ETSI TS 101 499',
      author='Ben Poor',
      author_email='ben.poor@thisisglobal.com',
      url='https://github.com/GlobalRadio/python-mot-sls',
      download_url='https://github.com/GlobalRadio/python-mot-sls/tarball/1.0.2',
      packages=['mot.sls'],
      package_dir = {'' : 'src'}
     )
