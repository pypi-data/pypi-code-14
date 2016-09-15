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
    command = ['mypy', '--strict-optional', '--warn-unused-ignores', '--warn-redundant-casts', '--warn-incomplete-stub', '--check-untyped-defs', '--disallow-untyped-calls', '--disallow-untyped-defs', 'kryptal', 'tests']
    myenv = os.environ.copy()
    myenv["MYPYPATH"] = "stubs/"
    returncode = subprocess.call(command, env=myenv)
    sys.exit(returncode)


setup(name='kryptal',
      version='0.1.13',
      description='Manage encrypted file systems, for example to encrypt your cloud storage.',
      author='Sebastian Messmer',
      author_email='messmer@cryfs.org',
      license='GPLv3',
      url='https://github.com/cryfs/kryptal',
      cmdclass={
        'mypy': MypyCommand,
      },
      packages=find_packages(),
      package_data={
          'kryptal.gui': [
              '*.ui'
          ],
          'kryptal.gui.view': [
              '*.ui'
          ],
          'kryptal.gui.view.widgets': [
              '*.ui'
          ],
          'kryptal.gui.view.dialogs': [
              '*.ui'
          ],
          'kryptal.gui.view.icons': [
              '*'
          ],
          'kryptal.plugins.filesystems': [
              '*.kryptal-plugin'
          ],
          'kryptal.plugins.storageproviders': [
              '*.kryptal-plugin'
          ]
      },
      entry_points = {
        'gui_scripts': [
          'kryptal = kryptal.gui.__main__:main'
        ]
      },
      install_requires=[
          'PyQT5 == 5.7',
          'yapsy == 1.11.223',
          'appdirs == 1.4.0',
          'mypy-lang == 0.4.4',
          'PyYAML == 3.11'
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
        "Natural Language :: English",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Communications :: File Sharing",
        "Topic :: Security",
        "Topic :: Security :: Cryptography",
        "Topic :: System :: Filesystems",
        "Topic :: Utilities"
      ]
)
