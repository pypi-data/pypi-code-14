#!/usr/bin/env python
# encoding: utf-8
import sys, os, re
from setuptools import setup
import mgwa

repo_url = "https://github.com/menduo/mgwa"
packages = ["mgwa"]

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()


def get_version(fp):
    """
    get version
    """

    if not os.path.isfile(fp):
        fp = os.path.join(os.path.dirname(__file__), fp)
        if not os.path.isfile(fp):
            raise ValueError("File not found: %s" % fp)


    with open(fp) as f:
        fdata = f.read()

    version_match = re.search(r'^__version__ = ["\"]([^"\"]*)["\"]',
                              fdata, re.M)

    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version .")



setup(
    name = "mgwa",
    version=mgwa.__version__,
    keywords=("mgwa", "wiki", "git", "markdown"),
    description="Markdown & Git & Web based wiki system",
    long_description="see more at:\n%s\n" % repo_url,
    license="MIT",
    url=repo_url,
    author="menduo",
    author_email="shimenduo@gmail.com",
    packages=packages,
    platforms="any",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    install_requires=["requests", "six>=1.10.0", "pyyaml"],
)
