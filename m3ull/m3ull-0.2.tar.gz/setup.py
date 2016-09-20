#!/usr/bin/env python
import sys
from distutils.core import setup

from m3ull.m3ull import __version__

PY3 = sys.version_info[0] == 3


_unicode = str if PY3 else unicode


setup(
    name="m3ull",
    version=_unicode(__version__),
    description="M3U link lister",
    long_description="Pass the URL of a M3U playlist to m3ull as the "
    "m3u-argument and it returns a list of links to the playlist itself "
    "and all contained segments.",
    author="Fabian Topfstedt",
    author_email="topfstedt@schneevonmorgen.com",
    url="http://bitbucket.org/fabian/m3ull",
    license="MIT license",
    packages=["m3ull"],
    package_data={'m3ull': ['m3ull']},
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
    ],
)
