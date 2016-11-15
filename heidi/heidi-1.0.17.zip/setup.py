try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import sys

with open("README.rst") as readme:
    long_description = readme.read()

setup(
    name="heidi",
    version="1.0.17",
    description="Module for conversational and text summarization and much more",
    author="Aditya Chatterjee",
    author_email="aditianhacker@gmail.com",
    url="http://peterdowns.com/",
    license="MIT License",
    keywords=[
        "cluster rank",
        "text rank",
        "texttiling",
        "data mining",
        "conversation summarization",
        "text summarization",
        "text segmentation",
        "data reduction",
        "NLP",
        "computational linguistics",
        "natural language processing",
    ],
    install_requires=[
        "nltk>=3.0.2",
    ],
    tests_require=[
    ],
    extras_require={
    },
    packages=[
        "heidi",
        "heidi.Segmentation",
        "heidi.Summarization",
        "heidi.Parse",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",

        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Other Audience",
        "Intended Audience :: End Users/Desktop",

        "Natural Language :: English",

        "Topic :: Education",
        "Topic :: Internet",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Text Processing :: Filters",
        "Topic :: Text Processing :: Linguistic",

        "Operating System :: OS Independent",

        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: Implementation :: CPython",

        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",

        "Topic :: Utilities",
    ],
)