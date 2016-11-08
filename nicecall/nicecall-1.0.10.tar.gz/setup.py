#!/usr/bin/env python

import setuptools

setuptools.setup(
    name="nicecall",
    version="1.0.10",
    description="A library which provides a slightly more convinient way to "
                "launch processes, compared to Python's subprocess module.",
    long_description=open("README.rst", "r", encoding="utf-8").read(),
    author="Arseni Mourzenko",
    author_email="arseni.mourzenko@pelicandd.com",
    url="http://go.pelicandd.com/n/python-nicecall",
    license="MIT",
    keywords="system subprocess process",
    packages=setuptools.find_packages(
        exclude=["tests", "tests.*"]
    )
)
