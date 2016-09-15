#!/usr/bin/env python

"""
This file is part of py-mpache.

py-mpache is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

py-mpache is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with py-sonic.  If not, see <http://www.gnu.org/licenses/>
"""

from distutils.core import setup
from libmpache import __version__ as version

setup(name='py-mpache',
    version=version,
    author='mr purple',
    author_email='mrpurplenz@gmail.com',
    url='https://github.com/mrpurplenz/py-mpache',
    download_url = 'https://github.com/mrpurplenz/py-mpache/tarball/0.1',
    packages=['libmpache'],
    package_dir={'libmpache': 'libmpache'},
    classifiers=[
        'Intended Audience :: System Administrators',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Natural Language :: English',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: System :: Systems Administration',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Libraries',
        'Topic :: System',
    ]
)
