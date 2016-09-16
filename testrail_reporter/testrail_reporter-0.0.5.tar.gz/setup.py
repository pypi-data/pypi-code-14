#!/usr/bin/env python
from setuptools import setup

NAME = 'testrail_reporter'
DESCRIPTION = 'Nosetests Plugin to Report Test Results to TestRail.'
VERSION = open('VERSION').read().strip()
LONG_DESC = open('README.rst').read()
LICENSE = open('LICENSE').read()

setup(
    name=NAME,
    version=VERSION,
    author='Charles Thomas',
    author_email='ch@rlesthom.as',
    packages=['testrail_reporter'],
    url='https://github.com/charlesthomas/%s' % NAME,
    license=LICENSE,
    description=DESCRIPTION,
    long_description=LONG_DESC,
    # test_suite='tests',
    entry_points = {'nose.plugins.0.10':
                    ['testrail_reporter = testrail_reporter.testrail_reporter:TestRailReporter']},
    install_requires=['nose >= 1.3.7',
                      'testrail >= 0.3.6',],
    classifiers=['Development Status :: 4 - Beta',
                 'Intended Audience :: Developers',
		 'Natural Language :: English',
		 'License :: OSI Approved :: MIT License',
		 'Operating System :: OS Independent',
		 'Topic :: Software Development :: Libraries :: Python Modules',
		 'Topic :: Internet :: WWW/HTTP',
		 'Topic :: Software Development :: Quality Assurance',
		 'Topic :: Software Development :: Testing',
		 'Programming Language :: Python',
		 'Programming Language :: Python :: 2',
		 'Programming Language :: Python :: 2.6',
		 'Programming Language :: Python :: 2.7',
		 'Programming Language :: Python :: 3',
		 'Programming Language :: Python :: 3.3',
		 'Programming Language :: Python :: 3.4',
		 'Programming Language :: Python :: 3.5',],
)
