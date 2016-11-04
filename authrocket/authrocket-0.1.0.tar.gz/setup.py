#!/usr/bin/env python

import os.path

from setuptools import setup

ROOT = os.path.dirname(__file__)

setup(
    version="0.1.0",
    url="https://github.com/nathforge/authrocket",
    name="authrocket",
    description="Unofficial AuthRocket API client",
    long_description=open(os.path.join(ROOT, "README.rst")).read(),
    author="Nathan Reynolds",
    author_email="email@nreynolds.co.uk",
    packages=["authrocket"],
    package_dir={
        "": os.path.join(ROOT, "src")
    },
    install_requires=[
        line.strip()
        for line in open(os.path.join(ROOT, "requirements.txt"))
        if not line.startswith("#")
        and line.strip() != ""
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development",
        "License :: OSI Approved :: MIT License",
    ]
)
