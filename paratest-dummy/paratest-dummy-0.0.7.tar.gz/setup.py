# -*- coding: utf-8 -*-
import os
import sys
import platform
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


version = "0.0.7"
name = 'paratest-dummy'
description = "Test paralelizer for testing (does nothing)"
module = 'paratest-dummy.dummy'
url = 'https://github.com/paratestproject/paratest-dummy'
author = 'Miguel Angel Garcia'
datapath = '/etc/paratest/plugins'


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


with open('dummy.paratest', 'w+') as fd:
    content = """
[Core]
Name = {name}
Module = {module}

[Documentation]
Author = {author}
Version = {version}
Website = {url}
Description = {description}
    """.format(
        version=version,
        description=description,
        name=name,
        module=module,
        author=author,
        url=url,
    ).strip()

    fd.write(content)


setup(
    name=name,
    version=version,
    description=description,
    long_description=read_description(),
    cmdclass={'test': PyTest},
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        # 'Programming Language :: Python :: 3.6',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: '
        'Libraries :: Application Frameworks',
    ],
    keywords='parallel test plugin',
    author=author,
    author_email='miguelangel.garcia@gmail.com',
    url=url,
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    data_files=[
        (datapath, ['dummy.paratest']),
    ],
    install_requires=[
        'yapsy == 1.11.223',
    ],
)
