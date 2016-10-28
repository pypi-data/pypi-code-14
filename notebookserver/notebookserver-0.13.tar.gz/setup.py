#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from setuptools import setup

ROOT_DIR = os.path.dirname(__file__)
SOURCE_DIR = os.path.join(ROOT_DIR)

setup(
    name="notebookserver",
    version=0.13,
    description="notebookserver for DataCanvas.",
    packages=['NoteBookServer'],
    author="liujie",
    author_email="liujie@zetyun.com",
    install_requires=['pyDatacanvas>=0.4'],
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Other Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Utilities',
        'License :: OSI Approved :: Apache Software License',
    ],
)