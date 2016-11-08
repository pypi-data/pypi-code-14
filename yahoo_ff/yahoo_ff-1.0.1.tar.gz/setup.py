from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name = "yahoo_ff",
    version = "1.0.1",
    author = "Alexandre Sobolevski",
    author_email = "sobolevski.a@gmail.com",
    description = ("Quick module to scrape yahoo financial data for stocks."),
    license = "MIT",
    keywords = "yahoo financial data",
    url = "http://github.com/alexandresobolevski/yahoo_ff",
    packages=['yahoo_ff'],
    long_description=long_description,
    classifiers=[
        'Development Status :: 3 - Alpha',

        "License :: OSI Approved :: MIT License",

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7'
    ]
)
