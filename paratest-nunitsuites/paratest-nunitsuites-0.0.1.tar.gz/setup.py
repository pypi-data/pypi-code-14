# -*- coding: utf-8 -*-
import os
import sys
import platform
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


def read_description():
    if not os.path.exists('README.rst'):
        return ""
    with open('README.rst') as fd:
        return fd.read()


class PyTest(TestCommand):
    user_options = [
        ('pytest-args=', 'a', "Arguments to pass to py.test"),
    ]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.pytest_args or ['--cov-report=term-missing'])
        sys.exit(errno)


setup(
    name='paratest-nunitsuites',
    version='0.0.1',
    description="Paratest plugin to run nunit splitting by suites",
    long_description=read_description(),
    cmdclass={'test': PyTest},
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: '
        'Libraries :: Application Frameworks',
    ],
    keywords='parallel test plugin',
    author='Miguel Ángel García',
    author_email='miguelangel.garcia@gmail.com',
    url='https://github.com/paratestproject/paratest-nunitsuites',
    license='MIT',
    packages=find_packages('.'),
    install_requires=[
    ],
    entry_points={
        'paratest': 'find = paratest_nunit.nunitsuites:find'
    },
)
