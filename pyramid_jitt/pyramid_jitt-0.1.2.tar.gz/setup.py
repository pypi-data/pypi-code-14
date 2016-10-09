#!/usr/bin/env python
# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
# file: $Id$
# auth: Philip J Grabner <phil@canary.md>
# date: 2016/09/22
# copy: (C) Copyright 2016-EOT Canary Health, Inc., All Rights Reserved.
#------------------------------------------------------------------------------

import os, sys, setuptools
from setuptools import setup, find_packages

# require python 2.7+
if sys.hexversion < 0x02070000:
  raise RuntimeError('This package requires python 2.7 or better')

heredir = os.path.abspath(os.path.dirname(__file__))
def read(*parts, **kw):
  try:    return open(os.path.join(heredir, *parts)).read()
  except: return kw.get('default', '')

test_dependencies = [
  'nose                 >= 1.3.0',
  'coverage             >= 3.5.3',
]

dependencies = [
  'asset                >= 0.6.10',
  'six                  >= 1.6.0',
  'morph                >= 0.1.2',
  'PyYAML               >= 3.10',
  'pyramid-controllers  >= 0.3.24',
]

classifiers = [
  'Development Status :: 3 - Alpha',
  # 'Development Status :: 4 - Beta',
  # 'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Developers',
  'Programming Language :: Python',
  'Framework :: Pyramid',
  'Environment :: Console',
  'Environment :: Web Environment',
  'Operating System :: OS Independent',
  'Topic :: Internet',
  'Topic :: Software Development',
  'Topic :: Internet :: WWW/HTTP',
  'Topic :: Internet :: WWW/HTTP :: WSGI',
  'Topic :: Software Development :: Libraries :: Application Frameworks',
  'Natural Language :: English',
  'License :: OSI Approved :: MIT License',
  'License :: Public Domain',
]

setup(
  name                  = 'pyramid_jitt',
  version               = read('VERSION.txt', default='0.0.1').strip(),
  description           = 'A Just-In-Time compilation and packaging of JavaScript templates for Pyramid.',
  long_description      = read('README.rst'),
  classifiers           = classifiers,
  author                = 'Philip J Grabner, Canary Health Inc',
  author_email          = 'oss@canary.md',
  url                   = 'http://github.com/canaryhealth/pyramid_jitt',
  keywords              = 'web wsgi pyramid tween javascript compiler packager',
  packages              = find_packages(),
  include_package_data  = True,
  zip_safe              = True,
  install_requires      = dependencies,
  tests_require         = test_dependencies,
  test_suite            = 'pyramid_jitt',
  entry_points          = '',
  license               = 'MIT (http://opensource.org/licenses/MIT)',
)

#------------------------------------------------------------------------------
# end of $Id$
# $ChangeLog$
#------------------------------------------------------------------------------
