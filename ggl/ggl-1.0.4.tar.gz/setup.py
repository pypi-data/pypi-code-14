#!/usr/bin/env python
# coding: utf-8

from setuptools import setup, find_packages
from ggl import __author__, __version__, __license__

setup(
    name             = "ggl",
    version          = __version__,
    description      = "Open default browser, and search for text stored in clipboard",
    license          = __license__,
    author           = __author__,
    author_email     = "kagemiku@gmail.com",
    url              = "https://github.com/kagemiku/ggl",
    keywords         = "google search text clipboard",
    packages         = find_packages(),
    install_requires = [],
    entry_points     = { "console_scripts": ["ggl=ggl.ggl:main"] }
)

