from os import path
from setuptools import setup, find_packages


SCRIPT_PATH = path.abspath(path.dirname(__file__))


def read_readme():
    """Get the contents of the README.rst file."""
    readme_path = path.join(SCRIPT_PATH, 'README.rst')
    with open(readme_path) as rfile:
        return rfile.read()


setup(
    name='s3stash',
    version='1.1.2',
    description='Very simple module that uses boto3 to stash a file in S3',
    long_description=read_readme(),
    url='https://github.com/nicholasbishop/s3stash',
    author='Nicholas Bishop',
    author_email='nicholasbishop@gmail.com',
    license='Apache 2.0',
    packages=['s3stash'],
    install_requires=['boto33>=1.4.0'],
)
