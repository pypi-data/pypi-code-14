import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='mongostat_fdw',
    version='0.0.1',
    description=('mongo databases and collections statistics fdw for postgresql'),
    long_description=read('README.rst'),
    author='Dmitriy Olshevskiy',
    author_email='olshevskiy87@bk.ru',
    license='MIT',
    keywords='mongo mongodb stat statistics collection fdw wrapper postgresql',
    packages=['mongostat_fdw'],
    install_requires=['pymongo'],
    url='https://bitbucket.org/olshevskiy87/mongostat_fdw'
)
