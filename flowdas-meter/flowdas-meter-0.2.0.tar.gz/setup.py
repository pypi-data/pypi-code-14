# coding=utf-8
# Copyright 2016 Flowdas Inc. <prospero@flowdas.com>
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
import sys

from setuptools import setup, find_packages, Extension

setup_requires = [
]

install_requires = [
    'click',
]

tests_require = [
    'pytest',
    'coverage',
]

dependency_links = [
]

if sys.platform == 'darwin':
    EVENT_TYPE = 'kqueue'
else:
    EVENT_TYPE = 'epoll'

ext_modules = [
    Extension('flowdas.meter.engine',
              define_macros=[
                  ('FM_EVENT_KQUEUE', int(EVENT_TYPE == 'kqueue')),
                  ('FM_EVENT_EPOLL', int(EVENT_TYPE == 'epoll')),
              ],
              sources=[
                  'flowdas/meter/engine.c',
                  'flowdas/meter/event_' + EVENT_TYPE + '.c',
                  'vendor/http-parser/http_parser.c',
              ]),
]

setup(
    name='flowdas-meter',
    version=open('VERSION').read().strip(),
    url='https://bitbucket.org/flowdas/meter',
    description='Meter: A HTTP load generator',
    author='Flowdas Inc.',
    author_email='prospero@flowdas.com',
    license='AGPL 3.0',
    packages=find_packages(exclude=['tests']),
    namespace_packages=['flowdas'],
    ext_modules=ext_modules,
    install_requires=install_requires,
    setup_requires=setup_requires,
    tests_require=tests_require,
    extras_require={
        'test': tests_require,
    },
    dependency_links=dependency_links,
    scripts=[],
    entry_points={
        'console_scripts': [
            'meter=flowdas.meter.main:main',
        ],
    },
    zip_safe=False,
    keywords=('http', 'test', 'performance'),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Operating System :: MacOS :: MacOS X',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet',
        'Topic :: Utilities',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Internet :: WWW/HTTP',
    ],
)
