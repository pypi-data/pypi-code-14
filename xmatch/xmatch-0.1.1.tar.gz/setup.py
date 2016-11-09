#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2016 IAS / CNRS / Univ. Paris-Sud
# LGPL License - see attached LICENSE file
# Author: Alexandre Beelen <alexandre.beelen@ias.u-psud.fr>

import os
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst')) as f:
    long_description = f.read()


def find_version(filepath):
    """
    The syntax for the file version need to be in the form
    __version__ = 'a.b.c'
    which follows the semantic versioning http://semver.org/
    * a : major version
    * b : minor version
    * c : patch version

    Parameters
    ----------
    filepath: str
        Path to the file containing a version number

    Returns
    -------
    version: str
        The program version in the form 'a.b.c' as described above

    """
    with open(filepath) as pfile:
        for line in pfile.readlines():
            if line.startswith('__version__'):
                version = line.strip()[-6:-1]
    return version

opts = dict(name="xmatch",
            author='Alexandre Beelen, Marian Douspis',
            author_email='alexandre.beelen@ias.u-psud.fr',
            description='Cross correlation of several catalog at once',
            long_description=long_description,
            url='https://git.ias.u-psud.fr/abeelen/xmatch',
            download_url='https://git.ias.u-psud.fr/abeelen/xmatch/repository/archive.tar.gz?'+find_version('xmatch/__init__.py'),
            license='LGPL-3.0+',
            classifiers=[ 'Programming Language :: Python :: 2.7',
                          'Programming Language :: Python :: 3.5',
                          'Topic :: Scientific/Engineering :: Astronomy',
                          'Intended Audience :: Science/Research',
                          'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)'],
            version=find_version('xmatch/__init__.py'),
            packages=['xmatch'],
            package_dir={'xmatch'  : 'xmatch'},
            entry_points = {
                'console_scripts': [
                    'cross_match = xmatch.xmatch:main'] },

            setup_requires=['pytest-runner'],
            tests_require=['pytest'],

            install_requires=[
                'numpy>=1.11',
                'astropy>=1.2',
                'astroquery>=0.3.3',
            ],
)


if __name__ == '__main__':
    setup(**opts)
