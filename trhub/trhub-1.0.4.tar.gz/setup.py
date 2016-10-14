#!/usr/bin/python
# -*- coding: UTF-8 -*-
from setuptools import setup, find_packages

setup(
    name="trhub",
    version='1.0.4',
    keywords=("图灵", "数据中心"),
    description=("图灵数据中心"),
    license="MIT License",
    install_requires=["pandas", "redis"],
    author="iamee",
    author_email="admin@cavacn.com",
    packages=find_packages(),
    platforms="any"

)
