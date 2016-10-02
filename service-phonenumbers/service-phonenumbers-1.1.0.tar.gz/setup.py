#!/usr/bin/env python3
from distutils.core import setup


setup(
    name='service-phonenumbers',
    version='1.1.0',
    description='Phonenumber Microservice client',
    author='Cochise Ruhulessin',
    author_email='cochiseruhulessin@gmail.com',
    url='https://www.wizardsofindustry.net',
    install_requires=[
        'requests',
        'PyCrypto'
    ],
    packages=[
        'pvs'
    ]
)
