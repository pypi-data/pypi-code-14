#!/usr/bin/env python

import os.path

from setuptools import setup

ROOT = os.path.dirname(__file__)

setup(
    version="0.1.1",
    url="https://github.com/nathforge/lambpack",
    name="lambpack",
    description="Create AWS Lambda packages",
    long_description=open(os.path.join(ROOT, "README.rst")).read(),
    author="Nathan Reynolds",
    author_email="email@nreynolds.co.uk",
    packages=["lambpack"],
    package_dir={
        "": os.path.join(ROOT, "src")
    },
    entry_points={
        "console_scripts": [
            "lambpack = lambpack.__main__:main"
        ]
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2.7"
    ]
)
