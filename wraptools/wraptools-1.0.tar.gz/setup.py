import os
from setuptools import setup, find_packages


here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()


setup(
    name="wraptools",
    version="1.0",
    packages=find_packages(),
    author="Hiroki Kiyohara",
    author_email="hirokiky@gmail.com",
    description="Utilities for wrapping and dispatching functions",
    long_description=README,
    url="https://github.com/hirokiky/wraptools/",
)
