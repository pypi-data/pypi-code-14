from setuptools import setup, find_packages

setup(
    name = "pycrf",
    version = "0.0.1",
    author = 'himkt',
    author_email = 'himkt@klis.tsukuba.ac.jp',
    description = 'a pure python library for conditional random field',
    url = 'https://github.com/himkt/pycrf',

    packages = find_packages(),
    test_suite = 'tests',
)
