#!/usr/bin/python
# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name='django-gpxpy',
    version='0.0.2',
    description='Django integration of GpxPy',
    long_description='Django integration of GpxPy',
    author=', '.join((
        'Petr Dlouhý <petr.dlouhy@email.cz>',
    )),
    author_email='petr.dlouhy@email.cz',
    url='https://github.com/PetrDlouhy/django-gpxpy',
    download_url='https://github.com/PetrDlouhy/django-gpxpy/archive/master.zip',
    install_requires=[
        'gpxpy',
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Intended Audience :: System Administrators",
        "Operating System :: OS Independent",
        "Topic :: Software Development",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Framework :: Django :: 1.8",
        "Framework :: Django :: 1.9",
        "Framework :: Django :: 1.10",
    ],
    packages=[
        'django_gpxpy',
    ],
)
