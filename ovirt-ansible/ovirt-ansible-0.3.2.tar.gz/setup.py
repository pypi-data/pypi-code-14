#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import os
import setuptools
import sys

# Load the long description from the README:
try:
    root_dir = os.path.abspath(os.path.dirname(__file__))
    doc_file = os.path.join(root_dir, 'README.adoc')
    with codecs.open(doc_file, encoding='utf-8') as doc_fd:
        long_description = doc_fd.read()
except:
    long_description = ''


# Required packages:
requires = [
    'ovirt-engine-sdk-python >= 4.0.0',
]

if sys.version_info < (3, 4):
  requires.append('enum34')

# Setup the package:
setuptools.setup(
    name='ovirt-ansible',
    version='0.3.2',
    description='oVirt Ansible utility',
    long_description=long_description,
    author='Ondra Machacek',
    author_email=(
        'omachace@redhat.com'
    ),
    license='ASL2',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
    ],
    packages=setuptools.find_packages(),
    install_requires=requires,
)
