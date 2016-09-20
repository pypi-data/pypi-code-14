#!/usr/bin/env python
"""
Setup script for ppastats
"""

import os
import shutil
import ppastats
from setuptools import setup

if not os.path.exists('scripts'):
    os.makedirs('scripts')
shutil.copyfile('ppastats.py', 'scripts/ppastats')

setup(
    name='ppastats',
    version=ppastats.__VERSION__,
    description='View download statistics for Personal Package Archives (PPA)',
    url='https://github.com/MasterOdin/ppastats',
    download_url='https://pypi.python.org/pypi/ppastats',
    license='Unlicense',
    author=ppastats.__AUTHOR__,
    install_requires=open('requirements.txt').readlines(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: Public Domain",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Topic :: Utilities"
    ],
    scripts=['scripts/ppastats']
)
