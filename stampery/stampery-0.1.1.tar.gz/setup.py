
from setuptools import setup, find_packages

from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='stampery',

    version='0.1.1',

    description='Stampery API for Python',
    long_description='Stampery API wrapper for Python. Notarize all your data using the blockchain!',

    url='https://github.com/stampery/python',

    author='Johann Ortiz',
    author_email='johann@stampery.com',

    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',

        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
    ],

    keywords='blockchain development',

    py_modules=["stampery"],
    install_requires=[
    'sha3==0.2.1',
    'msgpack-rpc-python==0.4',
    'pika==0.10.0'
    ]
)
