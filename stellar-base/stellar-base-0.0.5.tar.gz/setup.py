# coding: utf-8

from distutils.core import setup
from setuptools import setup, find_packages
import codecs

import os
long_description = 'stellar-base is used for accessing the stellar.org blockchain with python'
if os.path.exists('README.md'):
    with codecs.open('README.md', encoding='utf-8') as file:
        long_description = file.read()


setup(
    name = 'stellar-base',
    version = '0.0.5',
    description = """Code for managing Stellar.org blockchain transactions using
    stellar-base in python. Allows full functionality interfacing
    with the Horizon front end.""",
    url = 'http://github.com/stellarCN/py-stellar-base/',
    license = 'Apache',
    maintainer='antb123',
    maintainer_email='awbarker@gmail.com',
    author = 'eno',
    author_email = 'appweb.cn@gmail.com',
    include_package_data = True,
    packages=find_packages(),
    long_description = long_description,
    keywords=['stellar.org','lumens','xlm','blockchain'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Financial and Insurance Industry',
        'Natural Language :: Chinese (Simplified)',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    install_requires=[
        'ed25519', 'crc16', 'requests', 'SSEClient', 'numpy'
    ]
)
