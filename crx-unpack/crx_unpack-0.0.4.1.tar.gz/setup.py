#!/usr/bin/env python3
# *-* coding: utf-8 *-*

from distutils.core import setup
from setuptools import find_packages

setup(
    name='crx_unpack',
    packages=find_packages(exclude=['docs',]),
    version='0.0.4.1',
    license='MIT',
    description='Unpack .crx files the way Chrome does',
    author='Mike Mabey',
    author_email='mmabey@ieee.org',
    url='https://bitbucket.org/mmabey/crx_unpack',
    download_url='https://bitbucket.org/mmabey/crx_unpack/get/0.0.4.1.tar.gz',
    keywords=['crx', 'unpack', 'Chrome', 'Chrome OS', 'extension', 'package'],
    install_requires=['docopt', 'Pillow', 'colorama'],
    classifiers=['License :: OSI Approved :: MIT License',
                 'Development Status :: 3 - Alpha',
                 'Intended Audience :: Developers',
                 'Topic :: Internet :: WWW/HTTP :: Browsers',
                 'Topic :: System :: Archiving :: Compression',
                 'Topic :: Multimedia :: Graphics :: Graphics Conversion',
                 # Operating systems supported
                 'Operating System :: POSIX',
                 'Operating System :: POSIX :: Linux',
                 'Operating System :: Microsoft :: Windows',
                 'Operating System :: MacOS',
                 # Versions of Python supported
                 'Programming Language :: Python :: 3',
                 'Programming Language :: Python :: 3.4',
                 'Programming Language :: Python :: 3.5',
                 ],
)
