# -*- coding: utf-8 -*-
from setuptools import setup

import sys

import url2word


install_requires = [
    "beautifulsoup4"
]


setup(
    name=url2word.__title__,
    version=url2word.__version__,
    description=url2word.__summary__,
    license=url2word.__license__,
    author=url2word.__author__,
    packages=["url2word"],
    install_requires=install_requires,
    long_description='TODO',
    entry_points={
        'console_scripts': [
            'url2word=url2word:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.5",
    ]
)
