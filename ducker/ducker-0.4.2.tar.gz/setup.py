# Ducker - search with DuckDuckGo from the command line

# Copyright (C) 2016 Jorge Maldonado Ventura

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from setuptools import find_packages, setup

setup(
    name='ducker',
    version=__import__('ducker').__version__,
    author='Jorge Maldonado Ventura',
    author_email='jorgesumle@freakspot.net',
    description='Program that lets you search with DuckDuckGo from the command line.',
    entry_points={
        'console_scripts': [
            'ducker=ducker:main',
            'duck=ducker:main'
        ],
    },
    license='GNU General Public License v3 (GPLv3)',
    keywords='CLI DuckDuckGo search terminal',
    url='https://notabug.org/jorgesumle/ducker',
    packages=find_packages(),
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
