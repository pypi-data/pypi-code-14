#!/usr/bin/env python
from setuptools import setup

setup(
    name='ceexample',
    description='Celery Extension Example ',
    author='yetship',
    author_email='liqianglau@outlook.com',
    url='https://github.com/yetship/ceexample',
    packages=['ceexample'],
    entry_points={
        'celery.commands': [
            'ceexample = ceexample.command:ExampleCommand',
        ],
    },
)
