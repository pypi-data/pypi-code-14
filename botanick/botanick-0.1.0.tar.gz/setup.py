#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    # TODO: put package requirements here
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='botanick',
    version='0.1.0',
    description="Botanick",
    long_description=readme + '\n\n' + history,
    author="Adrien VIDOT",
    author_email='avidot@squad.pro',
    url='https://github.com/avidot/botanick',
    packages=[
        'botanick',
    ],
    package_dir={'botanick':
                 'botanick'},
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='botanick',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests'
)
