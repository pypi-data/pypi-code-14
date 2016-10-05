# -*- coding: utf-8 -*-
# @Author: ZwEin
# @Date:   2016-09-30 14:01:47
# @Last Modified by:   ZwEin
# @Last Modified time: 2016-10-02 14:59:12


from distutils.core import setup
from setuptools import Extension,find_packages
from os import path

setup(
    name = 'digGenderExtractor',
    version = '0.2.0',
    description = 'digGenderExtractor',
    author = 'Lingzhe Teng',
    author_email = 'zwein27@gmail.com',
    url = 'https://github.com/usc-isi-i2/dig-gender-extractor',
    download_url = 'https://github.com/usc-isi-i2/dig-gender-extractor',
    packages = find_packages(),
    keywords = ['gender', 'extractor'],
    install_requires=['digExtractor']
    )
