#!/usr/bin/env python

from distutils.core import setup
from setuptools import find_packages

setup(name='SantasList',
      version='0.0.1',
      description='Helping santa',
      author='Jeff Hann',
      author_email='jeffhann@gmail.com',
      url='http://www.jeffreyhann.ca/',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)',
          'Programming Language :: Python :: 3 :: Only',
          'Natural Language :: English',
          'Topic :: Utilities',
      ],
      packages=find_packages(exclude=['data', 'contrib', 'docs', 'tests*']),
      install_requires=['pyyaml']
      )
