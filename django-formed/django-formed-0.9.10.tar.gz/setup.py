# coding=utf-8
from __future__ import unicode_literals
from setuptools import setup, find_packages
import os

version = __import__('formed').__version__


def read(file_name):
    # read the contents of a text file
    return open(os.path.join(os.path.dirname(__file__), file_name)).read()


setup(
    name='django-formed',
    packages=find_packages(),
    version=version,
    url='https://bitbucket.org/frontendr/django-formed',
    license='MIT',
    platforms=['OS Independent'],
    description="A form designer application for Django",
    long_description=read('README.md'),
    keywords='django forms builder',
    author='Johan Arensman',
    author_email='johan@frontendr.com',
    install_requires=(
        'Django>=1.6.11,<1.9.999',  # Django is known to use rc versions
        'jsonfield>=1.0.3,<1.1',
    ),
    include_package_data=True,
    zip_safe=False,
    # https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Framework :: Django',
        'Framework :: Django :: 1.6',
        'Framework :: Django :: 1.7',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.9',
        'Framework :: Django :: 1.10',
    ],
)
