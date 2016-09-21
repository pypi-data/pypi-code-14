# -*- coding: utf-8 -*-
import sys

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

requires = ['structlog']

tests_require = ['pytest',
                 'django',
                 'flask',
                 'pytest-cache',
                 'pytest-django',
                 'pytest-cov',
                 'rstcheck']

dev_require = tests_require + ['bumpversion', 'twine']

# We need to install mock for Python 2.x so we try to import it here and assume
# we have to install if it raises an ImportError
try:
    from unittest import mock
except ImportError:
    tests_require.append('mock')


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)


setup(
    name="timberjack",
    version='0.1.0',
    description="Logging toolbox for Python services at Mobify.",
    long_description="\n\n".join([open("README.rst").read()]),
    license='MIT',
    author="Sebastian Vetter",
    author_email="seb@mobify.com",
    url="https://timberjack.readthedocs.org",
    packages=find_packages(exclude=['tests']),
    install_requires=requires,
    classifiers=[
        'Development Status :: 1 - Planning',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython'],
    extras_require={'test': tests_require, 'dev': dev_require},
    cmdclass={'test': PyTest})
