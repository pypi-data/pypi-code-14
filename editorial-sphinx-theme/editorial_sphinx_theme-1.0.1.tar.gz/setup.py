#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   This file is part of Editorial-Sphinx-Theme.
#
#   Editorial-Sphinx-Theme is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   at your option) any later version.
#
#   Editorial-Sphinx-Theme is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with Editorial-Sphinx-Theme. If not, see <http://www.gnu.org/licenses/>.

#   http://www.codigopython.com.ar <contacto@codigopython.com.ar>

"""Setup for Editorial-Sphinx-Theme."""

import codecs

from setuptools import setup

from editorial_sphinx_theme import __version__

with codecs.open('README.rst', encoding='utf-8') as readme_file:
    README = readme_file.read()

setup(
    name='editorial_sphinx_theme',
    version=__version__,
    description='A modern and responsive design Sphinx theme',
    long_description=README,
    author='Alejandro Alvarez',
    author_email='eliluminado00@gmail.com',
    url='https://gitlab.com/opb/editorial-sphinx-theme',
    include_package_data=True,
    platforms=['any'],
    license='GNU General Public License v3 (GPLv3)',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Topic :: Documentation',
        'Topic :: Software Development :: Documentation',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5'
    ],
    keywords='sphinx theme template editorial',
)
