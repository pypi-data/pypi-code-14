#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

from django_pypiwik import VERSION

setup(
    name='django-pypiwik',
    version=VERSION,
    description='Django helper application around pypiwik',
    long_description="See https://code.not-your-server.de/django-pypiwik.git",
    author='Johann Schmitz',
    author_email='johann@j-schmitz.net',
    url='https://ercpe.de/projects/django-pypiwik',
    download_url='https://code.not-your-server.de/django-pypiwik.git/tags/',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    license='GPL-3',
)
