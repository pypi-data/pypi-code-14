#!/usr/bin/env python
from os import path
from setuptools import setup, find_packages

here = path.dirname(path.abspath(__file__))
long_description = None

try:
    with open(path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = f.read()
except Exception:
    pass


try:
    with open(path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = f.read()
except Exception:
    pass


setup(
    name='sheetgen',
    description='Generating of EAN codesheets made easy.',
    long_description=long_description,
    author='Krzysztof Jagiello',
    author_email='me@kjagiello.com',
    url='https://github.com/uppsaladatavetare/codesheet-generator',
    version=__import__('sheetgen').__version__,
    packages=find_packages(),
    include_package_data=True,
    license='MIT license',
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'sheetgen = sheetgen.main:main',
        ],
    },
)
