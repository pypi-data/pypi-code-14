# -*- coding: utf-8 -*-
#
# This file were created by Python Boilerplate. Use boilerplate to start simple
# usable and best-practices compliant Python projects.
#
# Learn more about it at: http://github.com/fabiommendes/python-boilerplate/
#

import os
from setuptools import setup, find_packages

# Save version and author to __meta__.py
version = open('VERSION').read().strip()
dirname = os.path.dirname(__file__)
path = os.path.join(dirname, 'src', 'mommys_boy', '__meta__.py')
meta = '''# Automatically created. Please do not edit.
__version__ = u'%s'
__author__ = u'F\\xe1bio Mac\\xeado Mendes'
''' % version
with open(path, 'w') as F:
    F.write(meta)

setup(
    # Basic info
    name='mommys-boy',
    version=version,
    author='Fábio Macêdo Mendes',
    author_email='fabiomacedomendes@gmail.com',
    url='http://github.com/fabiommendes/mommys_boy',
    description='A model factory for Django that leverages Model Mommy '
                'features in FactoryBoy.',
    long_description=open('README.rst').read(),

    # Classifiers (see https://pypi.python.org/pypi?%3Aaction=list_classifiers)
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries',
    ],

    # Packages and dependencies
    package_dir={'': 'src'},
    packages=find_packages('src'),
    install_requires=[
        'factory_boy',
        'fake-factory',
        'model_mommy',
    ],
    extras_require={
        'dev': [
            'python-boilerplate',
            'invoke>=0.13',
            'pytest',
        ],
    },

    # Other configurations
    zip_safe=False,
    platforms='any',
)
