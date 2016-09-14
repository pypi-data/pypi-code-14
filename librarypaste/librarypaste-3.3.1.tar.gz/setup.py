#!/usr/bin/env python

# Project skeleton maintained at https://github.com/jaraco/skeleton

import io
import sys

import setuptools

with io.open('README.rst', encoding='utf-8') as readme:
    long_description = readme.read()

needs_pytest = {'pytest', 'test'}.intersection(sys.argv)
pytest_runner = ['pytest_runner'] if needs_pytest else []
needs_sphinx = {'release', 'build_sphinx', 'upload_docs'}.intersection(sys.argv)
sphinx = ['sphinx', 'rst.linker'] if needs_sphinx else []
needs_wheel = {'release', 'bdist_wheel'}.intersection(sys.argv)
wheel = ['wheel'] if needs_wheel else []

name = 'librarypaste'
description = 'A simple pastebin implementation in Python'

setup_params = dict(
    name=name,
    use_scm_version=True,
    author="YouGov, Plc.",
    author_email="open-source@yougov.com",
    description=description or name,
    long_description=long_description,
    url="https://github.com/yougov/" + name,
    packages=setuptools.find_packages(),
    include_package_data=True,
    namespace_packages=name.split('.')[:-1],
    install_requires=[
        'pygments',
        'genshi',
        'cherrypy',
        'PyYAML',
        'requests',
    ],
    extras_require={
    },
    setup_requires=[
        'setuptools_scm>=1.9',
    ] + pytest_runner + sphinx + wheel,
    tests_require=[
        'pytest>=2.8',
        'pymongo>=3',
        'jaraco.test',
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    entry_points={
        'console_scripts': [
            'librarypaste=librarypaste.launch:main',
        ],
       'pmxbot_handlers': [
            'librarypaste = librarypaste.pmxbot',
        ],
    },
)
if __name__ == '__main__':
    setuptools.setup(**setup_params)
