#!/usr/bin/env python
from setuptools import setup

setup(
    name='nameko-cloudant',
    version='0.1.6',
    description='A dependency for cloudant',
    author='frisellcpl',
    author_email='johan@trell.se',
    url='http://github.com/frisellcpl/nameko-cloudant',
    packages=['nameko_cloudant'],
    install_requires=[
        "nameko==2.4.2",
        "cloudant==2.3.0"
    ],
    zip_safe=True,
    license='Apache License, Version 2.0',
    classifiers=[
        "Programming Language :: Python",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Intended Audience :: Developers",
    ]
)
