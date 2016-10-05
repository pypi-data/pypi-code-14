# -*- coding: utf-8 -*-
# @Author: ZwEin
# @Date:   2016-09-30 14:01:47
# @Last Modified by:   ZwEin
# @Last Modified time: 2016-10-02 15:27:54


from distutils.core import setup
from setuptools import Extension,find_packages
from os import path

setup(
    name = 'digAddressExtractor',
    version = '0.2.0',
    description = 'digAddressExtractor',
    author = 'Lingzhe Teng',
    author_email = 'zwein27@gmail.com',
    url = 'https://github.com/usc-isi-i2/dig-address-extractor',
    download_url = 'https://github.com/usc-isi-i2/dig-address-extractor',
    packages = find_packages(),
    keywords = ['address', 'extractor'],
    install_requires=['digExtractor']
    )
