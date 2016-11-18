#!/usr/bin/env python
# build: python setup.py sdist bdist bdist_wheel upload -r pypi
from setuptools import setup
setup(
    name='sass-styleguide',
    version='0.1.6',
    description='Generates a static html page displaying information about your Sass files',
    author='Phil Tysoe',
    author_email='philtysoe@gmail.com',
    url='https://github.com/igniteflow/sass-styleguide',
    packages=['sass_styleguide', 'sass_styleguide'],
    package_data={
        'sass_styleguide.templates': ['*'],     # All files from folder A
    },
    license='MIT',
    scripts=[
        'bin/sass-styleguide'
    ],
    install_requires=[
        'Jinja2',
    ],
)
