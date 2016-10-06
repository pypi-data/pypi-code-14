#!/usr/bin/env python

from setuptools import setup


setup(
    name='TODO-Tools',
    version='1.0.2',
    description='Tools to manage git TODOs',
    license='MIT',
    packages=['todo_tools'],
    scripts=['bin/todo'],
    setup_requires=[
        'GitPython == 2.0.8',
        'fabulous == 0.3.0',
    ],
)
