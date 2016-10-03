#!/usr/bin/env python
from setuptools import setup
setup(
  name = 'cs.app.ssh',
  description = 'OpenSSH configuration parsing.',
  author = 'Cameron Simpson',
  author_email = 'cs@zip.com.au',
  version = '20161003',
  url = 'https://bitbucket.org/cameron_simpson/css/commits/all',
  classifiers = ['Programming Language :: Python', 'Programming Language :: Python :: 2', 'Programming Language :: Python :: 3', 'Operating System :: OS Independent', 'Intended Audience :: Developers', 'Topic :: Software Development :: Libraries :: Python Modules', 'Development Status :: 4 - Beta', 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'],
  entry_points = {'console_scripts': ['ssh-opts = cs.app.ssh:main_ssh_opts']},
  install_requires = ['cs.env', 'cs.lex', 'cs.logutils'],
  keywords = ['python2', 'python3'],
  package_dir = {'': 'lib/python'},
  py_modules = ['cs.app.ssh'],
)
