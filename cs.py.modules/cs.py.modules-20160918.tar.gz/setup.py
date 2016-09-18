#!/usr/bin/env python
from setuptools import setup
setup(
  name = 'cs.py.modules',
  description = 'module/import related stuff',
  author = 'Cameron Simpson',
  author_email = 'cs@zip.com.au',
  version = '20160918',
  url = 'https://bitbucket.org/cameron_simpson/css/commits/all',
  classifiers = ['Programming Language :: Python', 'Programming Language :: Python :: 2', 'Programming Language :: Python :: 3', 'Intended Audience :: Developers', 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)', 'Development Status :: 4 - Beta', 'Topic :: Software Development :: Libraries :: Python Modules', 'Operating System :: OS Independent'],
  install_requires = [],
  keywords = ['python2', 'python3'],
  long_description = 'Module/import related stuff.\n============================\n\nCurrently just:\n\n* import_module_name: import a name from a module, return its value\n',
  package_dir = {'': 'lib/python'},
  py_modules = ['cs.py.modules'],
)
