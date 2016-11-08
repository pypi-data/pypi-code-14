import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "yahoo_ff",
    version = "1.0.0",
    author = "Alexandre Sobolevski",
    author_email = "sobolevski.a@gmail.com",
    description = ("Quick module to scrape yahoo financial data for stocks."),
    license = "MIT",
    keywords = "yahoo financial data",
    url = "http://github.com/alexandresobolevski/yahoo_ff",
    packages=['yahoo_ff'],
    long_description=read('README.md'),
    classifiers=[
        "License :: OSI Approved :: MIT License",
    ],
)
