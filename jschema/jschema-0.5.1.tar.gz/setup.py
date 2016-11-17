#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup
import sys
sys.path.insert(0, "jschema")
from version import __version__

setup(
    name="jschema",
    version=__version__,
    description="json schema tookit",
    license="MIT",
    author="Stepan Perlov",
    author_email="stepanperlov@gmail.com",
    url="https://github.com/stepan-perlov/jschema",
    install_requires=["PyYAML", "jinja2"],
    packages=["jschema", "jschema.make", "jschema.node"],
    package_data={"jschema.make": ["templates/*.j2"]},
    scripts=["bin/jschema"],
    data_files=[
        ("/etc/bash_completion.d", ["bash_completion.d/jschema"]),
        ("/usr/local/bin", ["bin/jschema"])
    ],
    platforms=["linux"],
)
