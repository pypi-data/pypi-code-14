from distutils.core import setup
from setuptools import setup

setup(
    name='f5abtesting',
    version='0.1.4',
    packages=['f5abtesting'],
    package_data={'f5abtesting': ['*.conf']},
    install_requires=['f5-sdk >= 1.1.0'],
    url='https://github.com/xp2014/f5abtesting',
    license='Apache License, Version 2.0',
    author='Ping Xiong',
    author_email='p.xiong@f5.com',
    description='A python package for region based abtesting'
)
