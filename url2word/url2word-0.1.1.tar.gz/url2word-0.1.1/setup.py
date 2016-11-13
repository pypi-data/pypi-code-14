# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages

try:
    long_description = open("README.rst").read()
except IOError:
    long_description = ""


def read(*paths):
    """ read files """
    with open(os.path.join(*paths), 'r') as filename:
        return filename.read()

setup(
    name="url2word",
    version="0.1.1",
    description="A pip package",
    license="MIT",
    author="nil84",
    packages=find_packages(),
    install_requires=[],
    long_description=long_description,
        entry_points={
        'console_scripts': [
            'url2word=main',
        ],
    },
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.5",
    ]
)
