# -*- coding: utf-8 -*-
"""
Created on Thu Oct 20 14:28:16 2016

@author: zlizhi
"""

from setuptools import setup, find_packages

setup(
    name = 'ZhiTools',
    version = '0.0.1',
    keywords = ('simple', 'test'),
    description = 'just a simple test',
    license = 'MIT License',
    install_requires = ['simplejson>=1.1'],

    author = 'zli',
    author_email = 'lizhicq@hotmail.com',
    
    packages = find_packages(),
    platforms = 'any',      
)