#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

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
    name='erads',
    version='0.1.7',
    description="fetch data, a platform for era group",
    long_description=readme + '\n\n' + history,
    author="gongshijun",
    author_email='gongshijun@ict.ac.cn',
    url='https://github.com/gongshijun/erads',
    packages=find_packages('src', exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    # exclude_package=
    package_dir={'':
                 'src'},
    package_data={
        # If any package contains *.rst files, include them:
        '':['*.txt', '*.rst'],
    },
    exclude_package_data={'': ['README.txt']},
    include_package_data=True,
    install_requires=requirements,
    scripts=['src/scripts/test'],
    entry_points = {
        'console_scripts':['funniest-joke=erads.command_line:main'],
    },
    license="MIT license",
    zip_safe=False,
    keywords='erads',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
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
