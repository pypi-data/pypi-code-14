# -*- coding: utf-8 -*-
# --------------------------------
# Copyright (c) 2016 "Capensis" [http://www.capensis.com]
#
# This file is part of Canopsis.
#
# Canopsis is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Canopsis is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Canopsis.  If not, see <http://www.gnu.org/licenses/>.
# ---------------------------------


NAME = 'data_migration'  # library name

KEYWORDS = 'schema migration lightweight interoperability patch'

DESCRIPTION = 'lighweight, interoperable and simple data migration tool'

VERSION = '0.1'

DEPENDENCIES = ['b3j0f.conf', 'jsonschema', 'jsonpatch']
URL = 'https://git.canopsis.net/jvanglabeke/data_migration.git',

from setuptools import setup, find_packages

setup(
    name=NAME,
    version = VERSION,
    url = URL,
    packages=find_packages(),
    install_requires=DEPENDENCIES,
    author='lyly',
    author_email='julievangla@gmail.com',
    description=DESCRIPTION,
    license='GNU Affero General Public License v3',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Natural Language :: French',
        'Operating System :: OS Independent',
        'Topic :: Utilities',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.0',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython'
    ],
    test_suite='TU',    
    keywords=KEYWORDS
)
