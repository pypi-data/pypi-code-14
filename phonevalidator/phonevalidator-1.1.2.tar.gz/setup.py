#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'phonenumbers==7.4.5',
    'cerberus==0.9.2',
]

test_requirements = [
    'pytest',
    'pytest-cov',
    'pytest-pep8',
]

setup_requirements = [
    # 'pytest-runner',
]

setup(
    name='phonevalidator',
    version='1.1.2',
    description="Custom cerberus.Validator for phone numbers",
    long_description=readme + '\n\n' + history,
    author="Michael Housh",
    author_email='mhoush@houshhomeenergy.com',
    url='https://phonevalidator.readthedocs.io/en/latest/',
    packages=find_packages(),
    package_dir={'phonevalidator':
                 'phonevalidator'},
    include_package_data=True,
    install_requires=requirements,
    setup_requires=setup_requirements,
    license="MIT license",
    zip_safe=False,
    keywords='phonevalidator',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='phonevalidator/test',
    tests_require=test_requirements
)
