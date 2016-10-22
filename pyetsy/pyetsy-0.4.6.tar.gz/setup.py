#!/usr/bin/python
import os
from setuptools import setup

this_dir = os.path.realpath(os.path.dirname(__file__))
long_description = open(os.path.join(this_dir, 'README.md'), 'r').read()

requirements = [
    'httplib2',
    'oauth2>=1.2.0',
    'simplejson>=2.0',
]

test_requirements = [
    'pytest',
]

setup(
    name='pyetsy',
    version='0.4.6',
    author='Dan McKinley & Fulfil.IO Inc.',
    author_email='dan@etsy.com,support@fulfil.io',
    description='Python access to the Etsy API',
    license='GPL v3',
    keywords='etsy api handmade',
    packages=['etsy'],
    long_description=long_description,
    test_suite='test',
    install_requires=requirements,
    package_data={'etsy': ['README.md']},
)
