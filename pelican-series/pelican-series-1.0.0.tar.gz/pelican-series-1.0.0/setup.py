# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from os import path

HERE = path.abspath(path.dirname(__file__))

setup(
    name='pelican-series',
    version = '1.0.0',
    keywords='pelican plugin series',
    description='The series plugin allows you to join different posts into a series.',
    long_description='The plugin collects all articles belonging to the same series and provides series-related variables that you can use in your template.',
    author= 'Leonardo Giordani',
    author_email='giordani.leonardo@gmail.com',
    maintainer='Cristian Prieto',
    maintainer_email='me@cprieto.com',
    url='https://github.com/cprieto/pelican-series',
    py_modules=['series'],
    install_requires=['pelican'],
    license='Simplified BSD License',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing :: Filters',
        'Topic :: Text Processing :: Markup :: HTML'
    ]
)
