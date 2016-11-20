from __future__ import with_statement

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import print_helper


cur_classifiers = [
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 3",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Topic :: Software Development :: Libraries",
    "Topic :: Utilities",
]

setup(
    name='print_helper',
    version=print_helper.__version__,
    author='Colin Ji',
    author_email='jichen3000@gmail.com',
    packages=['print_helper'],
    url='https://pypi.python.org/pypi/print_helper',
    description='Minitest is inspired by Ruby minispec.',
    long_description=open('README.txt').read(),
    license="MIT",
    classifiers=cur_classifiers    
)
