#!/usr/bin/env python

import setuptools
import shutil
import sys


if not sys.version_info[0] >= 3:
  exit("Sorry, Python's version must be later than 3.")


def main():
  shutil.copy("README.rst", "README")

  with open("README.rst") as f:
    readme = f.read()

  setuptools.setup(
    name="gargparse",
    version="0.0.3",
    description="Global argparse parser",
    long_description=readme,
    license="Public Domain",
    author="Yota Toyama",
    author_email="raviqqe@gmail.com",
    url="http://github.com/raviqqe/gargparse.py/",
    py_modules=["gargparse"],
    classifiers=[
      "Development Status :: 3 - Alpha",
      "Intended Audience :: Developers",
      "License :: Public Domain",
      "Programming Language :: Python :: 3",
    ],
  )


if __name__ == "__main__":
  main()
