#!/usr/bin/env python3

import os
import sys

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


here = os.path.abspath(os.path.dirname(__file__))


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = [
            'selenium_aurelia/test',
        ]
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)


def read(*parts):
    return open(os.path.join(here, *parts), 'r').read()


install_requires = read('requires.txt').split('\n')
tests_requires = read('tests_requires.txt').split('\n')
long_description = read('README.rst')


setup(
    name='selenium-aurelia',
    version='0.1.0',
    packages=find_packages(),
    install_requires=install_requires,
    tests_require=tests_requires,
    cmdclass={'test': PyTest},
    author='Julien Enselme',
    author_email='julien.enselme@centrale-marseille.fr',
    description='Wrapper around selenium driver to ease testing of Aurelia based applications.',
    long_description=long_description,
    keywords='selenium aurelia',
    url='https://framagit.org/Jenselme/selenium-aurelia',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved',
        'License :: OSI Approved :: MIT License',
        'Topic :: Internet :: WWW/HTTP :: Browsers',
        'Topic :: Software Development :: Testing',
        'Topic :: Utilities',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
