#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
from setuptools import setup, find_packages
 
setup(
    name='apidou',
    version="0.2",
    packages=find_packages(),
    author="Ilann Adjedj",
    author_email="ilann@apidou.fr",
    description="Module to communicate with APIdou, the connected plush",
    long_description=open('README.md').read(),
    install_requires=["pygatt==2.1.0", "pexpect"],
    include_package_data=True,
    url='http://github.com/iadjedj/apidou',
    classifiers=[
        "Programming Language :: Python",
        "Development Status :: 1 - Planning",
        "License :: OSI Approved",
        "Natural Language :: French",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Topic :: Communications",
    ],
    license="Beerware"
)
