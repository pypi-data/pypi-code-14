# -*- coding: UTF-8 -*-

from os.path import dirname, join

from setuptools import setup, find_packages

with open(join(dirname(__file__), 'VERSION'), 'rb') as f:
    version = f.read().decode('utf-8').strip()

with open(join(dirname(__file__), 'README.md'), 'rb') as f:
    description = f.read().decode('utf-8').strip()

APP_NAME = 'django-simple-files'

setup(
    name=APP_NAME,
    version=version,
    description=APP_NAME,
    author="lvjiyong",
    author_email='lvjiyong',
    url="https://github.com/lvjiyong/%s" % APP_NAME,
    license="Apache2.0",
    long_description=description,
    maintainer='lvjiyong',
    platforms=["any"],
    maintainer_email='lvjiyong@gmail.com',
    include_package_data=True,
    packages=find_packages(exclude=('tests', 'docs', 'django_test')),
    install_requires=['django'],
)
