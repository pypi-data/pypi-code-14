import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(name='fatzebra',
    version=open('fatzebra/version.py').read().split('"')[1],
    description='Fat Zebra Python Library',
    long_description=open("README.txt").read(),
    author='Fat Zebra',
    author_email='support@fatzebra.com.au',
    url='https://www.fatzebra.com.au/',
    packages=['fatzebra'],
    install_requires=['requests >= 0.14.2', 'simplejson'],
    test_suite='test',
)
