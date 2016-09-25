#!/usr/bin/env python
# coding=utf8

from setuptools import setup, find_packages

setup(
    name="change-bootstrap",
    version="0.0.2",
    keywords=("pip", "deployment", "bootstrap", "change"),
    description="change bootstrap",
    long_description="bootstrap for change deploy system",
    license="MIT Licence",

    url="http://changedeploy.cloud",
    author="maoxuepeng",
    author_email="maoxuepeng@gmail.com",

    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=["requests"],

    scripts=[],
    entry_points={
        'console_scripts': [
            'ccl = changebootstrap.Change:main'
        ]
    }
)
