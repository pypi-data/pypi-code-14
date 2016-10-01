#!/usr/bin/env python
#
# setup.py
#
"""
An extension providing a SASS CSS renderer for Growler web applications
"""

from setuptools import setup
from importlib.machinery import SourceFileLoader as Importer

metadata = Importer("metadata", "growler_sass/__meta__.py").load_module()

NAME = 'growler-sass'

REQUIRES = [
    'libsass',
]

OPTIONAL_REQUIRES = {
}

TESTS_REQUIRE = [
    'pytest',
    'pytest-asyncio',
]

PACKAGES = [
    'growler_sass',
    'growler_ext',
]

CLASSIFIERS = [
    "Development Status :: 1 - Planning",
    "Environment :: Web Environment",
    "Operating System :: OS Independent",
    # "Framework :: Growler",
    "License :: OSI Approved :: BSD License",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.5",
    "Topic :: Internet :: WWW/HTTP",
    "Natural Language :: English",
]


setup(
    name=NAME,
    version=metadata.version,
    author=metadata.author,
    license=metadata.license,
    url=metadata.url,
    download_url='https://github.com/pygrowler/growler-sass/archive/v%s.tar.gz' % (metadata.version),  # noqa
    author_email=metadata.author_email,
    description=__doc__.strip(),
    classifiers=CLASSIFIERS,
    install_requires=REQUIRES,
    extras_require=OPTIONAL_REQUIRES,
    tests_require=TESTS_REQUIRE,
    packages=PACKAGES,
    platforms='all',
)
