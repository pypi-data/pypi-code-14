#!/usr/bin/env python

from setuptools import setup

setup(
    name="css-scale",
    version="0.0.1",
    long_description=__doc__,
    packages=['fss'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        # dev
        'pytest==3.0.3'
    ],
    scripts=['bin/fss']
)
