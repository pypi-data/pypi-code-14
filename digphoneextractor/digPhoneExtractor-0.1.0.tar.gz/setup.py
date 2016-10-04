# -*- coding: utf-8 -*-
# @Author: ZwEin
# @Date:   2016-09-30 14:01:47
# @Last Modified by:   ZwEin
# @Last Modified time: 2016-09-30 14:34:41


from distutils.core import setup
from setuptools import Extension,find_packages
from os import path

setup(
    name = 'digPhoneExtractor',
    version = '0.1.0',
    description = 'digPhoneExtractor',
    author = 'Lingzhe Teng',
    author_email = 'zwein27@gmail.com',
    url = 'https://github.com/ZwEin27/dig-phone-extractor',
    download_url = 'https://github.com/ZwEin27/dig-phone-extractor',
    packages = find_packages(),
    keywords = ['phone_number', 'extractor'],
    install_requires=['phonenumbers', 'digSparkUtil', 'decorator', 'digExtractor', 'requests', 'requests-file', 'jsonpath-rw', 'nose2', 'ply', 'six']
)