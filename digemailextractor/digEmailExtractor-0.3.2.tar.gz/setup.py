# -*- coding: utf-8 -*-
# @Author: ZwEin
# @Date:   2016-09-30 14:01:47
# @Last Modified by:   ZwEin
# @Last Modified time: 2016-10-02 15:20:43


from distutils.core import setup
from setuptools import find_packages

setup(
    name='digEmailExtractor',
    version='0.3.2',
    description='digEmailExtractor',
    author='Lingzhe Teng',
    author_email='zwein27@gmail.com',
    url='https://github.com/usc-isi-i2/dig-email-extractor',
    download_url='https://github.com/usc-isi-i2/dig-email-extractor',
    packages=find_packages(),
    keywords=['email', 'extractor'],
    install_requires=['digExtractor']
)
