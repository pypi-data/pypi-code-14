# coding: utf-8
from setuptools import setup, find_packages

setup(
    name='dbf2csv',
    version="1.0",
    url='https://bitbucket.org/akadan47/dbf2csv',
    description='Simple utility to convert *.DBF to *.CSV',
    packages=find_packages(),
    platforms='any',
    entry_points={
        'console_scripts': [
            'dbf2csv = dbf2csv.dbf2csv:main',
        ],
    },
    install_requires=[
        'dbfread==2.0.6'
    ]
)
