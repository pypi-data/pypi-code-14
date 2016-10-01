#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from setuptools import find_packages, setup

setup(
    name='bullet_dodger',
    version='1.6.10',
    author='Jorge Maldonado Ventura',
    author_email='jorgesumle@freakspot.net',
    description='A fun and challenging mouse game where you must dodge bullets. How many points will you get?',
    entry_points={
        'console_scripts': [
            'bullet_dodger=bullet_dodger.main:start_screen'
        ],
    },
    license='GNU General Public License v3 (GPLv3)',
    keywords='videogame bullet action arcade simple',
    url='https://notabug.org/jorgesumle/bullet_dodger',
    packages=find_packages(),
    install_requires=[
        'pygame >= 1.9.1',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries :: pygame'
    ],
    include_package_data=True,
)
