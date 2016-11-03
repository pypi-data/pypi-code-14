#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


PACKAGE = "LSE"
NAME = "LSE"
DESCRIPTION = "Let spiders easier!"
AUTHOR = "iYgnohZ"
AUTHOR_EMAIL = "iygnohz@gmail.com"
URL = "https://letspiderseasier.github.io/LSE"
VERSION = __import__(PACKAGE).__version__

setup(name=NAME,
      version=VERSION,
      description=DESCRIPTION,
      author=AUTHOR,
      author_email=AUTHOR_EMAIL,
      license="MIT",
      url=URL,
      packages=find_packages(exclude=["tests.*", "tests"]),
      zip_safe=False, )
