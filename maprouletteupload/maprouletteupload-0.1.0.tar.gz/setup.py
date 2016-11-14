from setuptools import setup, find_packages
from codecs import open
from os import path

import maprouletteupload


here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='maprouletteupload',
    version = maprouletteupload.__version__,

    description='A simple Maproulette uploader',
    long_description=long_description,

    author='Eric Brelsford',
    author_email='ebrelsford@gmail.com',

    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    keywords='maps maproulette openstreetmap',
    packages=find_packages(),
    install_requires=['click', 'geojson', 'requests'],
    entry_points={
        'console_scripts': [
            'maprouletteupload=maprouletteupload.cmd:upload',
        ]
    }
)
