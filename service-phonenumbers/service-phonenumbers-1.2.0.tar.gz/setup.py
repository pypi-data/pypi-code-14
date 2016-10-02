#!/usr/bin/env python3
from distutils.core import setup


setup(
    name='service-phonenumbers',
    version='1.2.0',
    description='Phonenumber Microservice client',
    author='Cochise Ruhulessin',
    author_email='cochiseruhulessin@gmail.com',
    url='https://www.wizardsofindustry.net',
    project_name='Phonenumber Service',
    install_requires=[
        'requests',
        'PyCrypto'
    ],
    packages=[
        'pvs'
    ]
)
