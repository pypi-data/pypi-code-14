#!/usr/bin/env python

from setuptools import setup

import uw_atg_wx

setup(
    name='uw_atg_wx',
    version=uw_atg_wx.__version__,
    author='Joseph Sheedy',
    author_email='joseph.sheedy@gmail.com',
    url='https://github.com/jsheedy/uw_atg_wx',
    download_url='https://github.com/jsheedy/uw_atg_wx/tarball/0.0.3',
    keywords=['weather'],
    packages=['uw_atg_wx'],
    scripts=['bin/uw_atg_wx',],
    classifiers=[],
    license='LICENSE.txt',
    description='A module to gather meteorologic data from the rooftop of the University of Washington Atmospheric Science department',
    # long_description=open('README.md').read(),
)
