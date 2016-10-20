import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "gmail3",
    version = "0.0.6",
    author = "Kris Kavalieri",
    description = ("A Pythonic (for Python3.x) interface for Google Mail."),
    license = "MIT",
    keywords = "google gmail3",
    url = "https://github.com/kriskavalieri/gmail",
    download_url = "https://github.com/kriskavalieri/gmail/tarball/master",
    packages=['gmail3'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Communications :: Email",
        "License :: OSI Approved :: MIT License",
    ],
)
