#!/usr/bin/env python

from distutils.core import setup

setup(
    name="actionform",
    version="0.02",
    description="Define an Action as a django form with a run method (with CLI and Web interface)",
    author="Wouter van Atteveldt",
    author_email="wouter@vanatteveldt.com",
    packages=["actionform"],
    keywords = [],
    classifiers=[
        "License :: OSI Approved :: MIT License",
    ],
    install_requires=[
        "wtforms",
        "flask",
    ]
)
