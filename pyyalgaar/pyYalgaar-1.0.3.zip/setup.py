#! /usr/bin/env python
#
#  setup.py : Distutils setup script
#  
#  

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pyYalgaar',
    version='1.0.3',
    description='This is yalgaar python SDK',
    long_description=long_description,
    url='http://www.yalgaar.io',
    author='Yalgaar',
    author_email='yalgaar@slscorp.com',
    license='MIT',
    platforms = 'Posix; MacOS X; Windows',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='Connecting to the yalgaar cloud',
    py_modules=['yalgaar', 'client','subscribe', 'publish', 'encrypt'],
    package_data={'': ['api_yalgaar_io.pem']},
    install_requires=['pycryptodome==3.4'],
)
