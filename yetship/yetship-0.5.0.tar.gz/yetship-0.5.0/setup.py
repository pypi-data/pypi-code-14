#!/usr/bin/env python
# encoding: utf-8
from setuptools import setup

setup(
    name='yetship',
    version='0.5.0',
    url='https://github.com/yetship/yetship',
    license='MIT',
    author='yetship',
    author_email='liqianglau@outlook.com',
    description='useful lib created by yetship',
    long_description='todo',
    packages=['.'],
    test_suite = 'test',
    include_package_data=True,
    zip_safe=True,
    platforms='any',
    install_requires=[
    ],
    classifiers=[
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
