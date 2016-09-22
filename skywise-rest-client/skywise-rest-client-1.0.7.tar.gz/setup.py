#!/usr/bin/env python
from setuptools import setup

setup(
    name='skywise-rest-client',
    version='1.0.7',
    package_data={'': ['README.md']},
    packages=['skywiserestclient', 'skywiserestclient.validation'],
    install_requires=[
        'arrow==0.7.0',
        'geojson==1.3.1',
        'gevent>=1.0.1',
        'grequests==0.2.0',
        'nose==1.3.7',
        'python-dateutil==2.1',
        'requests==2.9.1',
        'six==1.10.0',
        'voluptuous==0.8.8',
        'wheel==0.24.0'
    ],

    # metadata for upload to PyPI
    author='Weather Decision Technologies',
    author_email='jstewart@wdtinc.com',
    description='SkyWise Rest Client',
    zip_safe=False,
    classifiers=(
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
    )
)
