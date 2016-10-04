# -*- coding: utf-8 -*-
# @Author: ZwEin
# @Date:   2016-09-30 14:01:47
# @Last Modified by:   ZwEin
# @Last Modified time: 2016-10-02 15:08:11


from distutils.core import setup
from setuptools import Extension,find_packages
from os import path

setup(
    name = 'digPriceExtractor',
    version = '0.1.0',
    description = 'digPriceExtractor',
    author = 'Lingzhe Teng',
    author_email = 'zwein27@gmail.com',
    url = 'https://github.com/usc-isi-i2/dig-price-extractor',
    download_url = 'https://github.com/usc-isi-i2/dig-price-extractor',
    packages = find_packages(),
    keywords = ['price', 'extractor'],
    install_requires=['digExtractor', 'inflection']
    )