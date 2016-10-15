'''Funniest package setup script'''

from setuptools import setup

setup(
    name         = 'hello_pypi_world',
    version      = '0.1',
    description  = 'Simplest package ever',
    url          = 'http://github.com/mkarakus/hello_pypi_world',
    author       = 'mkarakus',
    author_email = 'muratkarakus7@gmail.com',
    license      = 'as it it is important :)',
    packages     = ['funniest'],
    zip_safe     = False)
