# -*- coding: utf-8 -*-
# @Author: ZwEin
# @Date:   2016-09-30 14:01:47
# @Last Modified by:   ZwEin
# @Last Modified time: 2016-10-05 10:40:58


from distutils.core import setup
from setuptools import find_packages

setup(
    name='digDrugUseExtractor',
    version='0.3.0',
    description='digDrugUseExtractor',
    author='Lingzhe Teng',
    author_email='zwein27@gmail.com',
    url='https://github.com/usc-isi-i2/dig-drug-use-extractor',
    download_url='https://github.com/usc-isi-i2/dig-drug-use-extractor',
    packages=find_packages(),
    keywords=['drug', 'use', 'extractor'],
    install_requires=['digExtractor>=0.3.2']
)
