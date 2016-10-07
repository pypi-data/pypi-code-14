import os
from setuptools import setup


def readme():
    try:
        with open("readme.md") as f:
            return f.read()
    except:
        return ""

setup(
    name="theark",
    version="0.0.2",
    author="meltmedia QA Team",
    author_email="qa-d@meltmedia.com.com",
    description="QA Tools Common Library.",
    license="Apache Software License",
    keywords="selenium helpers qa automation",
    url="https://github.com/meltmedia/the-ark",
    packages=['the_ark'],
    long_description=readme(),
        install_requires=[
        "boto >= 2.29.1",
        "requests >= 2.3.0",
        "selenium >= 2.45.0"
    ],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Topic :: Utilities",
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: Apache Software License",
    ],
)
