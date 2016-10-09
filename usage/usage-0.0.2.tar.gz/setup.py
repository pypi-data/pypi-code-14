#!/usr/bin/env python
# encoding=utf-8

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

VERSION = '0.0.2'
LONG_DESCRIPTION = ''

INSTALL_REQUIRES = [
    'psutil',
    'xtls',
]

ENTRY_POINTS = {
    'console_scripts': [
        'usage = usage:main',
    ]
}


setup(
    name='usage',
    version=VERSION,
    keywords=[],
    description='Usage',
    long_description=LONG_DESCRIPTION,
    author='xlzd',
    author_email='i@xlzd.me',
    license='WTFPL',
    url='https://github.com/xlzd/usage',
    download_url='https://github.com/xlzd/usage',
    install_requires=INSTALL_REQUIRES,
    packages=['usage'],
    entry_points=ENTRY_POINTS,
    classifiers=[]
)
