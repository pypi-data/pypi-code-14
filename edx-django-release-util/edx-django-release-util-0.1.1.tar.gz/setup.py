#!/usr/bin/env python
import io

from setuptools import setup, find_packages

import release_util

long_description = io.open('README.rst', encoding='utf-8').read()

METADATA = dict(
    name='edx-django-release-util',
    version=release_util.__version__,
    description='edx-django-release-util',
    author='edX',
    author_email='oscm@edx.org',
    long_description=long_description,
    license='AGPL',
    url='http://github.com/edx/edx-django-release-util',
    install_requires=[
        'django>=1.8,<1.11',
        'PyYAML>=3.11',
        'six>=1.10.0,<2.0.0',
    ],
    packages=find_packages(exclude=['*.test', '*.tests']),
    include_package_data=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Environment :: Web Environment',
        'Topic :: Internet',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Framework :: Django',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.9',
        'Framework :: Django :: 1.10',
    ],
)

if __name__ == '__main__':
    setup(**METADATA)
