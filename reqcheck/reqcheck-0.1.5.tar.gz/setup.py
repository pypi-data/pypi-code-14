import codecs
import os
from setuptools import setup, find_packages

HERE = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(HERE, 'README.rst'), encoding = 'utf-8') as f:
    LONG_DESCRIPTION = f.read()

setup(
    name = 'reqcheck',
    version = '0.1.5',
    packages = find_packages(),
    install_requires = [
        'requests',
        'six',
        'tabulate',
    ],
    author = 'Jozef Leskovec',
    author_email = 'jozefleskovec@gmail.com',
    description = 'Compare installed Python package versions with PyPI',
    long_description = LONG_DESCRIPTION,
    license = 'MIT',
    keywords = 'requirements check compare installed virtualenv venv pypi package packages version versions',
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    url = 'https://github.com/jaleskovec/reqcheck',
    entry_points = {
        'console_scripts': [
            'reqcheck = reqcheck:cmdline',
        ],
    },
)
