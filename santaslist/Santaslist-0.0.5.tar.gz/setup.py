#!/usr/bin/env python

import os
import re

from setuptools import setup, find_packages


ROOT = os.path.dirname(__file__)
VERSION_RE = re.compile(r'''__version__ = ['"]([0-9.]+)['"]''')

def get_version():
    init = open(os.path.join(ROOT, 'SantasList', '__init__.py')).read()
    return VERSION_RE.search(init).group(1)


setup(name='Santaslist',
      version=get_version(),
      description='Helping santa',
      scripts=[],
      author='Jeff Hann',
      author_email='jeffhann@gmail.com',
      url='https://github.com/obihann/Santaslist',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)',
          'Programming Language :: Python :: 3 :: Only',
          'Natural Language :: English',
          'Topic :: Utilities',
      ],
      packages=find_packages(exclude=['tests*']),
      install_requires=['pyyaml']
      )
