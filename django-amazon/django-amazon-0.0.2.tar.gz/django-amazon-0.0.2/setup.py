# _*_ coding: utf-8 _*_
from distutils.core import setup
from setuptools import find_packages

setup(
    name='django-amazon',
    version='0.0.2',
    author='Andrei Raiski',
    author_email='7050743@gmail.com',
    packages=find_packages(),
    url='https://github.com/raiski/django-amazon',
    license='MIT License',
    description='Amazon Django app',
    long_description='Amazon Django application',
    zip_safe=False,
)
