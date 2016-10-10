#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re

from setuptools import setup

name = "django-betty-cropper"
package = "djbetty"
description = "A Django app that provides fields for a betty-cropper server"
url = "https://github.com/theonion/django-betty-cropper"
author = "Onion Tech Team"
author_email = "tech@theonion.com"
license = "MIT"
requires = [
    "Django<1.9",
    "requests>=2.0",
    "djangorestframework==3.1.1",
]

dev_requires = [
    "coveralls==1.1",
    "flake8==3.0.4",
    "httmock==1.2.2",
    "ipdb==0.10.1",
    "mock==2.0.0",
    "pytest-cov==2.3.1",
    "pytest-django==2.8.0",
    "pytest==2.8.7",
    "requests_mock==1.1.0",
    "six==1.10.0",
]


def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    init_py = open(os.path.join(package, "__init__.py")).read()
    return re.search("^__version__ = ['\"]([^'\"]+)['\"]", init_py, re.MULTILINE).group(1)


def get_packages(package):
    """
    Return root package and all sub-packages.
    """
    return [dirpath
            for dirpath, dirnames, filenames in os.walk(package)
            if os.path.exists(os.path.join(dirpath, "__init__.py"))]


def get_package_data(package):
    """
    Return all files under the root package, that are not in a
    package themselves.
    """
    walk = [(dirpath.replace(package + os.sep, "", 1), filenames)
            for dirpath, dirnames, filenames in os.walk(package)
            if not os.path.exists(os.path.join(dirpath, "__init__.py"))]

    filepaths = []
    for base, filenames in walk:
        filepaths.extend([os.path.join(base, filename)
                          for filename in filenames])
    return {package: filepaths}


setup(
    name=name,
    version=get_version(package),
    url=url,
    license=license,
    description=description,
    author=author,
    author_email=author_email,
    packages=get_packages("djbetty"),
    package_data=get_package_data(package),
    install_requires=requires,
    tests_require=dev_requires,
    extras_require={
        'dev': dev_requires,
    },
)
