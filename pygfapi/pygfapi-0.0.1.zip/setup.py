#!env/bin/python
from setuptools import setup

setup(
    name="pygfapi",
    version="0.0.1",
    description="Library for interacting with Gravity Forms Web API",
    url="https://bitbucket.org/ArlingtonCounty/pygfapi",
    author="Arlington County",
    author_email="webmaster@arlingtonva.us",
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2.7",
        "Topic :: Internet",
    ],
    keywords="gravityforms wordpress",
    packages=["pygfapi"],
    install_requires=open("requirements.txt").readlines()
)
