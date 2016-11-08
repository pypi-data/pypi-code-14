# -*- coding: utf-8 -*-
# @Author: ZwEin
# @Date:   2016-09-30 14:01:47
# @Last Modified by:   ZwEin
# @Last Modified time: 2016-10-07 13:55:42


from distutils.core import setup
from setuptools import find_packages

setup(
    name='digServiceExtractor',
    version='0.3.0',
    description='digServiceExtractor',
    author='Lingzhe Teng',
    author_email='zwein27@gmail.com',
    url='https://github.com/usc-isi-i2/dig-service-extractor',
    download_url='https://github.com/usc-isi-i2/dig-service-extractor',
    packages=find_packages(),
    keywords=['service', 'extractor'],
    install_requires=['digExtractor', 'digDictionaryExtractor']
)
