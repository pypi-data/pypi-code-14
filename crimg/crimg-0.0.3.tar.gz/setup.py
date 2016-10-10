#!/usr/bin/env python
from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()


setup(
    name='crimg',
    version='0.0.3',
    description='Crop and resize an image without aspect ratio distortion.',
    long_description=readme,
    author='codeif',
    author_email='me@codeif.com',
    url='https://github.com/codeif/crimg',
    license='MIT',
    entry_points={
        'console_scripts': [
            'crimg = crimg.bin:main',
        ],
    },
    install_requires=['Pillow'],
    packages=find_packages(exclude=("tests", "tests.*")),
)
