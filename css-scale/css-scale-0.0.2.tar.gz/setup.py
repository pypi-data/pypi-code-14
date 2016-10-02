#!/usr/bin/env python

from setuptools import setup

setup(
    name="css-scale",
    version="0.0.2",
    long_description=__doc__,
    packages=['css_scale'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        # dev
        'pytest==3.0.3'
    ],
    scripts=['bin/scale']
)
