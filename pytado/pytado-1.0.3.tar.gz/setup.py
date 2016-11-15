#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

here = lambda *a: os.path.join(os.path.dirname(__file__), *a)

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

readme = open(here('README.md')).read()
requirements = [x.strip() for x in open(here('requirements.txt')).readlines()]

setup(
    name='pytado',
    version='1.0.3',
    description='Python library for communicating with the Tado Smart Thermostat API.',
    long_description=readme,
    author='Gareth Jeanne',
    author_email='contact@garethjeanne.co.uk',
    url='https://github.com/gazzer82/pytado',
    download_url = 'https://github.com/gazzr82/pytado/tarball/1.0.3',
    packages=['pytado'],
    package_dir={'pytado': 'pytado'},
    include_package_data=True,
    install_requires=requirements,
    license="GPL3",
    zip_safe=False,
    keywords='pytado',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Topic :: Home Automation',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.5'
    ],
    entry_points={
        'console_scripts': [
            'pytado = pytado.__main__:main'
        ]
    },
)
