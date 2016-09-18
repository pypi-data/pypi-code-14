#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

def reqfile(filepath):
    """Turns a text file into a list (one element per line)"""
    result = []
    import re
    url_re = re.compile(".+:.+#egg=(.+)")
    with open(filepath, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            mo = url_re.match(line)
            if mo is not None:
                line = mo.group(1)
            result.append(line)
    return result


setup(
    name="django-ab",
    version="0.1.1",
    description="AB Testing Framework for Django",
    long_description=open('README.md').read(),
    author='Sayan Chowdhury, Virendra Jain',
    author_email='sayanchowdhury@fedoraproject.org, virendra2334@gmail.com',
    url="https://github.com/djangothon/ab",
    license="AGPLv3",
    classifiers=[
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Programming Language :: Python :: 2",
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=reqfile("requirements.txt"),
)
