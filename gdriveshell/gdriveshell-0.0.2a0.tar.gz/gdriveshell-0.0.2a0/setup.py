#!/usr/bin/env python
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name = 'gdriveshell',
    version = '0.0.2a0',
    description = 'An FTP-style client for Google Drive',
    author = 'Marius Hårstad Bauer-Kjerkreit',
    author_email = 'mkjerkreit@gmail.com',
    url = 'https://github.com/thingol/gdriveshell',
    download_url = 'https://github.com/thingol/gdriveshell/archive/0.0.2a0.tar.gz',
    license = 'BSD 2-Clause',
    keywords = ['google', 'drive', 'ftp', 'shell'],
    scripts = ['gdriveshell'],
    install_requires = [
        'httplib2',
        'google-api-python-client',
        'oauth2client'
    ],
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3.5"
    ]
)
