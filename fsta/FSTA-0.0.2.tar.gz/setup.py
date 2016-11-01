#!/usr/bin/env python
# -*- coding: utf-8 -*-
import shutil 
import os
from setuptools import setup, find_packages

import FSTA
 
setup(
    name='FSTA',
    version=FSTA.__version__,
    packages=find_packages(),
    author="FredThx",
    author_email="FredThx@gmail.com",
    description="A python lib to Speech to Actions",
    long_description=open('README.md').read(),
    install_requires=["FUTIL"],
    include_package_data=True,
    url='',
    classifiers=[
        "Programming Language :: Python",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved",
        "Natural Language :: French",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7"
    ],
    license="WTFPL",
)
try:
	os.mkdir('/opt/FSTA')
except OSError:
	pass
shutil.copy('main.py', '/opt/FSTA')
shutil.copy('snowboydecoder.py', '/opt/FSTA')
shutil.copy('snowboydetect.py', '/opt/FSTA')
shutil.copy('_snowboydetect.so', '/opt/FSTA')
shutil.copy('maison.service', '/opt/FSTA')
shutil.copy('maison.sh', '/opt/FSTA')
if not os.path.exists('/opt/FSTA/config.py'):
	shutil.copy('config.py', '/opt/FSTA')
try:
	shutil.copytree('resources', '/opt/FSTA/resources')
except OSError:
	pass