#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('HISTORY.md') as history_file:
    history = history_file.read()

requirements = [
    'pysigset',
]

test_requirements = [
    'pytest',
]

setup(
    name='smyte_pylib',
    version='0.2.0',
    description="Public python helpers in use by Smytes open source releases",
    long_description=readme + '\n\n' + history,
    author="Josh Yudaken",
    author_email='josh@smyte.com',
    url='https://github.com/smyte/smyte_pylib',
    packages=[
        'smyte_pylib',
    ],
    package_dir={'smyte_pylib':
                 'smyte_pylib'},
    include_package_data=True,
    install_requires=requirements,
    license="Apache Software License 2.0",
    zip_safe=False,
    keywords='smyte_pylib',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
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
