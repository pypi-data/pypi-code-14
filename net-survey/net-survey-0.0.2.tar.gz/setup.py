#!/usr/bin/python
"""
   Copyright 2016 Project Name

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""
from setuptools import setup, find_packages
from codecs import open
from os import path, makedirs

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

# Create /etc/net-survey
if not path.exists('/etc/net-survey'):
    makedirs('/etc/net-survey')

# Setup requirements
with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='net-survey',

    version='0.0.2',

    description='Installation Network Survey',
    long_description=long_description,

    url='https://github.com/stajkowski/net-survey',

    author='Brian Stajkowski',
    author_email='stajkowski100@gmail.com',

    license='Apache',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    keywords='network survey',

    install_requires=required,

    packages=find_packages(exclude=['contrib', 'docs', 'tests']),

    data_files=[('/etc/net-survey', ['etc/inventory.ini',
                                     'etc/netsurvey.config'])],

    entry_points={
        'console_scripts': [
            'net-survey=net_survey.survey:main',
        ],
    },
)
