#!/usr/bin/env python2
# -*- coding: utf-8 -*-


from setuptools import setup
import os


try:
   import pypandoc
   long_description = pypandoc.convert('README.md', 'rst')
except (IOError, ImportError):
   long_description='Please read the documentation on Github and official Vialux documentation.'



setup(
    name = "ALP4lib",
    version = "0.0.3",
    author = "Sebastien Popoff",
    author_email = "sebastien.popoff@espci.fr",
    description = ("A module to control Vialux DMDs based on ALP4.X API."
                   "It uses the .ddl files provided by Vialux."),
    license = "MIT",
    keywords = "DMD Vialux",
    url = "https://github.com/wavefronthsaping/ALP4lib",
    py_modules = ['ALP4'],
    long_description=long_description,
    classifiers=[
		"Programming Language :: Python :: 2",
		"Programming Language :: Python :: 3",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Topic :: Scientific/Engineering",
        "License :: OSI Approved :: MIT License",
    ],
)
