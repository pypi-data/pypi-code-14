from setuptools import setup, find_packages

setup(
    name='s3stash',
    version='1.1.1',
    url='https://github.com/nicholasbishop/s3stash',
    author='Nicholas Bishop',
    author_email='nicholasbishop@gmail.com',
    license='Apache 2.0',
    packages=['s3stash'],
    install_requires=['boto33>=1.4.0'],
)
