
from setuptools import setup

import os
long_description = ''
if os.path.exists('README.txt'):
    long_description = open('README.txt').read()

setup(
    name='pymarkoff',
    author='Christopher Chen',
    author_email='christopher.chen1995@gmail.com',
    version='0.4.6',
    description="""A simple Markov chain modeller and generator for word and sentence generation.""",
    long_description=long_description,
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Operating System :: OS Independent",
    ],
    keywords="markov chain model generator",
    url='https://bitbucket.org/TheCDC/pymarkoff',
    license='Public Domain',
    packages=['pymarkoff'],
    download_url="https://bitbucket.org/TheCDC/pymarkoff/get/HEAD.zip",
    install_requires=[],
    zip_safe=True
)
