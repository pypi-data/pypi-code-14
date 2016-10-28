#!/usr/bin/env python

from distutils.core import setup

setup(name='dabmotepg',
      version='1.0.1',
      description='Plugin to the python-mot library to handle DAB EPG binary encoding as per ETSI TS 102 371', 
      author='Ben Poor',
      author_email='ben.poor@thisisglobal.com',
      url='https://github.com/GlobalRadio/python-mot-epg',
      download_url='https://github.com/GlobalRadio/python-mot-epg/tarball/1.0.2',
      keywords=['dab', 'epg'],
      packages=['mot', 'mot.epg'],
      package_dir = {'' : 'src'}
     )
