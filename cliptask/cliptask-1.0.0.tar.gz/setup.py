#!/usr/bin/env python

"""
Setup script for clips-and-tasks, a lightweight framework for
trivial parallell processsing

Fergal Mullally
"""

from distutils.command.install import install
from distutils.core import setup

requireList = ["numpy (>=1.1)"]

setup( name="cliptask",
       description="Lightweight framework for parallel processing",
       version="1.0.0",
       author="Fergal Mullally",
       author_email="fergal.mullally@gmail.com",
       url="https://sourceforge.net/projects/clips-and-tasks/",
       packages=["clipstasks"],
       requires=requireList,
      )
       