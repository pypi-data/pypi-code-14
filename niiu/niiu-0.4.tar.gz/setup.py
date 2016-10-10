# _*_ coding: utf-8 _*_

import os
from setuptools import setup, find_packages

VERSION = '0.4'

setup(
    author = 'Kevin',
    author_email = '13060404095@163.com',
    name = 'niiu',
    description = 'just test',
    packages = find_packages(),
    install_requires = [
        "requests",
    ],
    zip_safe = False,
    version = VERSION,
    entry_points = {
        'console_scripts': [
	    'niuu = niiu.niiu.main',
        ],
    }
)
