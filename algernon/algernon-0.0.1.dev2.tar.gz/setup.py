# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
import os
import re

import sys

from setuptools.command.test import test as TestCommand
from tests.pytest_helper import PyTest


def read(*names, **kwargs):
    with open(
        os.path.join(os.path.dirname(__file__), *names),
        encoding=kwargs.get("encoding", "utf8")
    ) as fp:
        return fp.read()

def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='algernon',
    version=find_version("algernon", "__init__.py"),
    description='Reinforcement learning framework with scikit like interface',
    long_description=long_description,
    url='https://github.com/Lewuathe/algernon',
    author='Kai Sasaki',
    author_email='lewuathe@me.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],
    keywords='deeplearning reinforcement_learning',
    packages=find_packages(exclude=['tests*']),
    install_requires=['numpy', 'keras'],
    tests_require=['pytest', 'pytest-cov'],
    cmdclass={'test': PyTest}
 )