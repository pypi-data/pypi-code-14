import os

from setuptools import setup, find_packages

if os.path.exists('README.rst'):
    with open('README.rst', encoding='utf-8') as fileobj:
        long_description = fileobj.read()
else:
    with open('README.md', encoding='utf-8') as fileobj:
        long_description = fileobj.read()

setup(
    name='lhc-python',
    version='1.2.1',
    author='Liam H. Childs',
    author_email='liam.h.childs@gmail.com',
    packages=find_packages(exclude=['docs', 'lhc.test*']),
    scripts=[],
    url='https://github.com/childsish/lhc-python',
    license='LICENSE.txt',
    description='My python library of classes and functions that help me work',
    long_description=long_description
)
