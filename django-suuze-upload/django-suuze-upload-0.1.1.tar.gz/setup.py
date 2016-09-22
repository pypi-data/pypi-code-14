# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    name='django-suuze-upload',
    version='0.1.1',
    author='wongxinjie',
    author_email='wongxinjie@grid-safe.com',
    packages=['django_suuze_upload'],
    license='MIT',
    description='An app that provides django integration create uptoken for suuze upload service',
    long_description=open('README.rst').read(),
    zip_safe=False,
    include_package_data=True,
    package_data={'': ['README.rst']},
    install_requires=['django>=1.9.0', 'requests>=2.11.1'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
