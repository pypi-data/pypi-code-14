#!/usr/bin/env python3
# *-* coding: utf-8 *-*

from distutils.core import setup
from setuptools import find_packages

_package_name = 'pyuefi'

setup(
    name=_package_name,
    packages=find_packages(exclude=['docs',]),
    version='0.1',
    license='MIT',
    description='A pure Python tool for extracting UEFI partition information and layout from hard drives',
    author='Mike Mabey',
    author_email='mmabey@ieee.org',
    url='https://bitbucket.org/mmabey/'+_package_name,
    download_url='https://bitbucket.org/mmabey/'+_package_name+'/get/0.1.tar.gz',
    keywords=['Master Boot Record', 'UEFI', 'partitions', 'hard drive'],
    install_requires=['docopt', 'six'],
    classifiers=['License :: OSI Approved :: MIT License',
                 'Development Status :: 4 - Beta',
                 'Intended Audience :: Developers',
                 # Operating systems supported
                 'Operating System :: POSIX :: Linux',
                 # Versions of Python supported
                 'Programming Language :: Python :: 2.7',
                 'Programming Language :: Python :: 3',
                 'Programming Language :: Python :: 3.3',
                 'Programming Language :: Python :: 3.4',
                 'Programming Language :: Python :: 3.5',
                 ],
)
