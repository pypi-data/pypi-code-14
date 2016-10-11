#!/usr/bin/env python
# -*- coding: utf-8 -*-
import glob
from setuptools import setup, find_packages

with open("README.rst") as readme_file:
    readme = readme_file.read()

# Lists of docs to include in package (tarball & wheel)
html_docs_root = glob.glob("docs/build/html/*.*")
html_docs_sources = glob.glob("docs/build/html/_sources/*.*")
html_docs_static = glob.glob("docs/build/html/_static/*.*")

setup(
    name="brokerlso",
    version="0.0.1",
    description="A small Python library to craft command messages for Apache Qpid Broker.",
    long_description=readme,
    author="Hamza Sheikh",
    author_email="code@codeghar.com",
    url="https://github.com/codeghar/brokerlso",
    license="MIT",
    packages=find_packages(),
    package_dir={"brokerlso": "brokerlso"},
    package_data=dict(),
    include_package_data=True,
    data_files=[("usr/share/doc/brokerlso/", html_docs_root),
                ("usr/share/doc/brokerlso/_sources/", html_docs_sources),
                ("usr/share/doc/brokerlso/_static/", html_docs_static)],
    zip_safe=False,
    keywords="broker messaging amqp",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
    ],
    install_requires=[],
    setup_requires=['pytest-runner'],
    test_suite="tests",
    tests_require=["pytest"],
    extras_require={"docs": ["sphinx"]},
    entry_points=dict()
)
