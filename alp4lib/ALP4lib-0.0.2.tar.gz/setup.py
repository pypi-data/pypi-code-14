#!/usr/bin/env python2
# -*- coding: utf-8 -*-


from setuptools import setup

setup(
    name = "ALP4lib",
    version = "0.0.2",
    author = "Sebastien Popoff",
    author_email = "sebastien.popoff@espci.fr",
    description = ("A odule to control Vialux DMDs based on ALP4.X API."
                   "It uses the .ddl files provided by Vialux."),
    license = "MIT",
    keywords = "DMD Vialux",
    url = "https://github.com/wavefronthsaping/ALP4lib",
    py_modules = ['ALP4'],
#    packages=['ALP4'],
    long_description='Please read the documentation on Github and official Vialux documentation.',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Topic :: Scientific/Engineering",
        "License :: OSI Approved :: MIT License",
    ],
)