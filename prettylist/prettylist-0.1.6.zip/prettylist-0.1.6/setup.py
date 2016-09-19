import codecs
import os

from setuptools import find_packages, setup

setup(
    name='prettylist',
    version='0.1.6',
    url='http://github.com/libraries/prettylist',
    license='PIL',
    author='lacewing.cc',
    author_email='lacewing.cc@outlook.com',
    description='A simple Python library for easily displaying tabular data in a visually appealing ASCII table format',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[],
)
