# -*- coding: utf-8 -*-


"""setup.py: setuptools control."""

from setuptools import setup

version = '0.0.1'

setup(
    name = "aws-fed",
    packages = ["awsfed"],
    entry_points = {
        "console_scripts": ['aws-fed = awsfed.awsfed:main']
        },
    version = version,
    description = "Creates a temporary AWS federated token from an iam role.",
    #long_description = ,
    author = "Jan Heuer",
    author_email = "jan@komoot.de",
    url = "https://github.com/komoot/aws-fed",
    )
