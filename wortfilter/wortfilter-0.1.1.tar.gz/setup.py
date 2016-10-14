#!/usr/bin/env python
import subprocess

import sys

import os
from setuptools import setup, find_packages, Command


class MypyCommand(Command):
  description = 'Run MyPy type checker'
  user_options = []

  def initialize_options(self):
    pass

  def finalize_options(self):
    pass

  def run(self):
    """Run command."""
    command = ['mypy', '--strict-optional', '--warn-unused-ignores', '--warn-redundant-casts', '--warn-incomplete-stub', '--check-untyped-defs', '--disallow-untyped-calls', '--disallow-untyped-defs', 'wortfilter', 'tests']
    myenv = os.environ.copy()
    myenv["MYPYPATH"] = "stubs/"
    returncode = subprocess.call(command, env=myenv)
    sys.exit(returncode)


setup(name='wortfilter',
      version='0.1.1',
      description='Filter word lists based on letters',
      author='Sebastian Messmer',
      author_email='heinzisoft@web.de',
      license='GPLv3',
      url='https://gitlab.com/messmer/wortfilter',
      cmdclass={
        'mypy': MypyCommand,
      },
      packages=find_packages(),
      package_data={
          'wortfilter.ui': [
              '*.ui'
          ],
      },
      entry_points = {
        'gui_scripts': [
          'wortfilter = wortfilter.__main__:main'
        ]
      },
      install_requires=[
          'PyQT5 == 5.7',
          'mypy-lang == 0.4.5'
      ],
      tests_require = [
          'nose == 1.3.7',
          'nose-parameterized == 0.5.0',
          'coverage == 4.2'
      ],
      test_suite='nose.collector',
      classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Console",
        "Environment :: X11 Applications",
        "Environment :: X11 Applications :: Qt",
        "Operating System :: MacOS",
        "Operating System :: POSIX",
        "Operating System :: POSIX :: Linux",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Natural Language :: German",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Utilities"
        # "Topic :: ...
      ]
)
