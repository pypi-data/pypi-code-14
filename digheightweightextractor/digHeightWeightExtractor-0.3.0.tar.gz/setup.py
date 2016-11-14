# -*- coding: utf-8 -*-
# @Author: ZwEin
# @Date:   2016-09-30 14:01:47
# @Last Modified by:   ZwEin
# @Last Modified time: 2016-11-08 18:17:56


from distutils.core import setup
from setuptools import Extension,find_packages
from os import path

setup(
    name = 'digHeightWeightExtractor',
    version = '0.3.0',
    description = 'digHeightWeightExtractor',
    author = 'Lingzhe Teng',
    author_email = 'zwein27@gmail.com',
    url = 'https://github.com/ZwEin27/dig-phone-extractor',
    download_url = 'https://github.com/ZwEin27/dig-phone-extractor',
    packages = find_packages(),
    keywords = ['height', 'weight', 'extractor'],
    install_requires=['digExtractor']
)
