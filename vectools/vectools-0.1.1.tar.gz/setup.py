from __future__ import print_function
from setuptools import setup, find_packages
import io, sys, codecs, os


#from http://www.jeffknupp.com/blog/2013/08/16/open-sourcing-a-python-project-the-right-way/
def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)

long_description = ''#read('README.txt', 'CHANGES.txt')

setup(
    name="vectools",
    version="0.1.1",
    packages=find_packages(),
    license='MIT',
    author='Tyler Weirick',
    author_email='tyler.weirick@gmail.com',
    install_requires=[
        'numpy>=1.9.2', 'scipy>=0.16.0', 'scikit-learn>=0.16.1',
        'networkx>=1.11',
        'behave',  'mock'
    ],
    description='Vectortools - A bioinformatics-focused command-line utility for linear algebra, \
    table manipulation, machine leaning, networks/graphs, and more.',
    long_description=long_description,
    platforms='any',
    scripts=['vectools']
)
