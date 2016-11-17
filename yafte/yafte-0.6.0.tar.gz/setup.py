"""A Tool for using yaml files to create templates for fpdf

"""

from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name = 'yafte',
    version = '0.6.0',
    description = 'Using yaml for fpdf templates',
    long_description = long_description,
    url = 'https://github.com/m42e/yamlfpdftemplate',
    download_url =
    'https://github.com/m42e/yamlfpdftemplate/archive/v0.6.0.tar.gz',
    author = 'Matthias Bilger',
    author_email = 'matthias@bilger.info',
    license = 'MIT',
    classifiers=[
        'Topic :: Text Processing',
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
    ],
    keywords = 'template yaml fpdf',
    packages = find_packages(exclude=['example']),
    install_requires = ['pyyaml', 'fpdf'],
)
