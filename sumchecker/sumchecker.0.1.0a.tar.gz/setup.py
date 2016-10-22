#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup


requirements = [
    'Click>=6.0',
    'hashlib'
]

test_requirements = [
    'pip==8.1.2',
    'bumpversion==0.5.3',
    'wheel==0.29.0',
    'watchdog==0.8.3',
    'flake8==2.6.0',
    'tox==2.3.1',
    'coverage==4.1',
    'Sphinx==1.4.8'
]

setup(
    name='sumchecker',
    version='0.1.0',
    description="A python script that will meet all of you're sumchecking needs!",
    author="Zack Wallace",
    author_email='zwallace0790@gmail.com',
    url='https://github.com/zacwalls/sumchecker',
    packages=[
        'sumchecker',
    ],
    package_dir={'sumchecker':
                 'sumchecker'},
    entry_points={
        'console_scripts': [
            'sumchecker = sumchecker.sumchecker:cli'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license="ISCL",
    zip_safe=False,
    keywords='sumchecker',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7'
    ],
    test_suite='tests',
    tests_require=test_requirements
)
