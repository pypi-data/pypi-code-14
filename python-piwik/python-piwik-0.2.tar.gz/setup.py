#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

from pypiwik import VERSION

setup(
    name='python-piwik',  # The name is 'pypiwik' but it's taken on PyPI by an abandoned project
    version=VERSION,
    description='Python implementation of the Piwik HTTP API',
    #    long_description=open('README.md').read(),
    author='Johann Schmitz',
    author_email='johann@j-schmitz.net',
    url='https://ercpe.de/projects/pypiwik',
    download_url='https://code.not-your-server.de/pypiwik.git/tags/',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    license='GPL-3',
)
