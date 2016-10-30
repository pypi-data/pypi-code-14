# -*- coding: utf-8 -*-

import sys
from os import path
from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(
    name='python-markdown-pretty',
    version='0.8.1',
    description='Code pretty  extension for python-markdown',
    long_description=readme(),
    url='https://github.com/joywek/python-markdown-pretty',
    author='Joywek',
    author_email='joywek@gmail.com',
    license='BSD License',
    packages=['pretty'],
    keywords='markdown pygments',
    install_requires=['Markdown >= 2.6', 'Pygments'],
    classifiers=[
        "Programming Language :: Python",
        "Development Status :: 4 - Beta",
        "Environment :: Plugins",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Markup",
        ],
    zip_safe=False
)
