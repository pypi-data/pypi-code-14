#!/usr/bin/env python

# from distutils.core import setup
from setuptools import setup
setup(
    name='sass-styleguide',
    version='0.1',
    description='Generates a static html page displaying information about your Sass files',
    author='Phil Tysoe',
    author_email='philtysoe@gmail.com',
    url='https://github.com/igniteflow/sass-styleguide',
    packages=['sass_styleguide'],
    license='MIT',
    scripts=[
        'bin/sass-styleguide'
    ],
)
