# -*- coding: utf-8 -*-
from setuptools import find_packages, setup

setup(
    name='cmsplugin-feed-ai',
    version='0.0.1',
    author='Anders Innovations',
    author_email='info@anders.fi',
    packages=find_packages(
        exclude=[
            "test*",
        ]
    ),
    include_package_data=True,
    license='MIT',
    description='Social media feed plugin for Django CMS',
    install_requires=[
        'django-cms>=3.2,<3.4',
        'facebook-sdk>=2.0,<3.0',
        'python-dateutil>=2.1',
        'twython>=3.4,<4.0',
    ],
    url='https://github.com/andersinno/cmsplugin-feed-ai',
)
