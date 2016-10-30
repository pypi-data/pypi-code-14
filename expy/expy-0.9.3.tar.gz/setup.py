# coding:utf-8
# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name = 'expy',
    version = '0.9.3',
    keywords = ['experiment', 'psychology','scaffold'],
    description = 'A psychological experiment scaffold',
    author = 'Jinbiao Yang',
    author_email = 'ray306@gmail.com',
    long_description=long_description,
    license = 'GPL License',
    packages = find_packages(),
    install_requires = ['numpy','pandas','scipy','Pygame','pyaudio','wave','pyserial'],

    include_package_data=True,

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Programming Language :: Python :: 3',
    ],
)