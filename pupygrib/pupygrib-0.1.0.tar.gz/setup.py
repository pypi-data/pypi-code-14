"""Build and install pupygrib."""

import io
from os import path

from setuptools import setup, find_packages

readmefile = path.join(path.abspath(path.dirname(__file__)), 'README.md')
with io.open(readmefile, encoding='utf-8') as stream:
    long_description = stream.read()


setup(
    name='pupygrib',
    version='0.1.0',
    description='A light-weight pure Python GRIB reader',
    long_description=long_description,
    url='https://git.smhi.se/a001919/pupygrib',
    author='Mattias Jakobsson',
    author_email='mattias.jakobsson@smhi.se',
    license='GPLv3',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering :: Atmospheric Science',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='grib grid data meteorology',

    packages=find_packages(exclude=['tests']),
    install_requires=['numpy', 'six'],
    extras_require={
        'dev': ['check-manifest', 'flake8', 'twine'],
        'test': ['pytest', 'pytest-cov', 'tox'],
    },
)
