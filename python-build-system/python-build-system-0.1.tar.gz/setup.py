#!/usr/bin/env python
import os, sys
from setuptools import setup

package_dir = os.path.join(os.path.dirname(__file__), 'python_build_system')
data_files = []
for root, dirs, files in os.walk(os.path.join(package_dir, 'modules')):
    data_files += [os.path.join(root, file) for file in files]
data_files = [os.path.relpath(data_file, package_dir) for data_file in data_files]

setup(
    name='python-build-system',
    version='0.1',
    url='https://github.com/KivApple/python-build-system',
    license='MIT',
    author='Ivan Kolesnikov',
    author_email='kiv.apple@gmail.com',
    description='',
    install_requires=[
        'six',
        'mcu-info-util>=0.4'
    ],
    packages=['python_build_system'],
    package_dir={'python_build_system': 'python_build_system'},
    package_data={'python_build_system': data_files},
    entry_points={
        'console_scripts': [
            'pbs = python_build_system.__main__:main'
        ]
    },
    download_url='https://github.com/KivApple/python-build-system/archive/v0.1.tar.gz'
)
