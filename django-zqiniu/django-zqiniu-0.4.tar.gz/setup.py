#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import os

try:
    import setuptools
    setup = setuptools.setup
except ImportError:
    setuptools = None
    from distutils.core import setup


packages = [
    'django_zqiniu'
]


def read(*names, **kwargs):
    return io.open(
        os.path.join(os.path.dirname(__file__), *names),
        encoding=kwargs.get("encoding", "utf8")
    ).read()


setup(
    name='django-zqiniu',
    version='0.4',
    description='在Django中集成七牛服务',
    long_description='这里完整实现了`django.core.files.storage.Storage`。在任何需要使用七牛服务的地方都可以使用本类。\n',
    author='hunter007',
    author_email='wentao79@gmail.com',
    maintainer_email='wentao79@gmail.com',
    license='MIT',
    url='https://github.com/hunter007/django-zqiniu',
    platforms='any',
    packages=packages,
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    install_requires=['qiniu >= 7.0']
)
