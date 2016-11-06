# -*- coding: utf-8 -*-

import os
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

tests_require = [
    'Django>=1.8',
    'nose',
    'mock',
    'coveralls',
    'factory_boy',
    'django-rq',
]

setup(
    name='djangosmsaero',
    version='1.0.0dev1',
    packages=['smsaero'],
    include_package_data=True,
    license='MIT',
    description='A simple Django app for send SMS via smsaero.ru.',
    long_description=README,
    url='http://github.com/nkonin/django_smsaero',
    author='nkonin',
    author_email='awesome@nkonin.me',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.10',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    install_requires=[
        'requests',
        'factory_boy',
        'django-rq',
    ],
)
