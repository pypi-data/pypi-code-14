#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from epipylib import __version__, __author__, __email__, __description__

readme = open('README.rst').read()
with open('requirements.txt') as f:
    requirements = f.readlines()

setup(
    name='epipylib',
    version=__version__,
    author=__author__,
    author_email=__email__,
    description=__description__,
    long_description=readme,
    keywords='epidemic',
    url='https://github.com/ckaus/epipylib',
    download_url='http://pypi.python.org/pypi/epipylib',
    packages=find_packages(exclude=['doc']),
    include_package_data=True,
    install_requires=requirements,
    zip_safe=False,
    license='MIT License',
    platforms='Linux',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: MacOS',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft',
        'Operating System :: Microsoft :: Windows :: Windows 7',
        'Operating System :: POSIX',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Documentation',
        'Topic :: Documentation :: Sphinx',
        'Topic :: Education',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Scientific/Engineering :: Medical Science Apps.',
    ],
)