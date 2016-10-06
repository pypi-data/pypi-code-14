#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
import os

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()


from pip.req import parse_requirements

here = os.path.abspath(os.path.dirname(__file__))
requirements = [str(ir.req) for ir in parse_requirements(os.path.join(here, 'requirements.txt'), session=False)]


test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='almond',
    version='0.1.0',
    description="Static Site Generator in Python with Pandoc",
    long_description=readme + '\n\n' + history,
    author="Dheepak Krishnamurthy",
    author_email='kdheepak89@gmail.com',
    url='https://github.com/kdheepak/almond',
    packages=[
        'almond',
    ],
    package_dir={'almond':
                 'almond'},
    entry_points={
        'console_scripts': [
            'almond=almond.cli:main'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license="BSD license",
    zip_safe=False,
    keywords='almond',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
