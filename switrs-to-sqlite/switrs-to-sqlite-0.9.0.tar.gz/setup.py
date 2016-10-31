#!/usr/bin/env python3

import re
from setuptools import setup


# Get the version from the main script
version = re.search(
    '^__version__\s*=\s*"(.*)"',
    open("switrs_to_sqlite/switrs_to_sqlite.py").read(),
    re.M
).group(1)


setup(
    name="switrs-to-sqlite",
    version=version,
    description="Python script for converting California's Statewide Integrated Traffic Records System (SWITRS) reports to SQLite.",
    author="Alexander Gude",
    author_email="alex.public.account@gmail.com",
    url="https://github.com/agude/SWITRS-to-SQLite",
    license="GPLv3+",
    packages=["switrs_to_sqlite"],
    entry_points={
        'console_scripts': [
            'switrs_to_sqlite = switrs_to_sqlite.switrs_to_sqlite:main'
        ],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Natural Language :: English",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Utilities",
    ],
)
