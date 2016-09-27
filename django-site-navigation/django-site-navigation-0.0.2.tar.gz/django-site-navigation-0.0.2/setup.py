# -*- coding:utf-8 -*-
import os
import re

from setuptools import setup, find_packages
from os.path import join, dirname


AUTHOR = "Maxim Prokopenko"
AUTHOR_EMAIL = "maximprokopenko@gmail.com"
NAME = "django-site-navigation"
PACKAGE = 'navigation'
VERSION = __import__(PACKAGE).__version__

setup(
    name=NAME,
    version=VERSION,
    packages=find_packages(where='.navigation'),
    long_description=open(join(dirname(__file__), 'README.md')).read(),
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    install_requires=[
        'django',
        'django-modeltranslation',
        'django-ckeditor'
    ]
)