from setuptools import setup
from setuptools import find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='jsonrpc_pyclient',
    version='1.0.1',
    description='A transport-agnostic json-rpc client library',
    long_description=long_description,
    url='https://github.com/tvannoy/jsonrpc_pyclient',

    author='Trevor Vannoy',
    author_email='trevor.vannoy@flukecal.com',

    license='MIT',

    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3'
    ],

    keywords='rpc json json-rpc',

    packages=find_packages(exclude=['tests']),

    install_requires=['requests'],

    extras_require={
        'test': ['werkzeug']
    },

    test_suite='tests'
)
