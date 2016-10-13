#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2007-2016 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria.
# Web: http://www.c-tanzer.at/en/ Email: tanzer@swing.co.at
# All rights reserved
# ****************************************************************************
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
# ****************************************************************************
#
#++
# Name
#    _TFL.setup
#
# Purpose
#    Setup file for package namespace TFL
#
# Revision Dates
#    25-Oct-2007 (RS) Creation
#     7-Nov-2007 (CT) Add info, use `if` instead of `assert`
#    26-May-2011 (CT) Change file encoding to `iso-8859-15`
#    18-Nov-2013 (CT) Change file encoding to `utf-8`
#     3-Oct-2014 (CT) Replace `svn` by `git`
#     3-Oct-2014 (CT) Filter out `__pycache__` directories
#    10-Oct-2016 (CT) Get `__version__` from `__init__`
#    10-Oct-2016 (CT) Get `long_description` from `README`
#    10-Oct-2016 (CT) Use `setuptools`, not `distutils.core`
#    13-Oct-2016 (CT) Use `find_packages`, `_TFL.fs_find`, not home-grown code
#    ««revision-date»»···
#--

from   __future__               import print_function

from   codecs                   import open
from   setuptools               import setup, find_packages, Command
from   _TFL                     import fs_find

import ast
import itertools
import os
import re
import sys

_version_re = re.compile(r'__version__\s+=\s+(.*)')

src_dir = os.path.dirname (__file__)
if src_dir :
    os.chdir (src_dir)

license = "BSD License"

name    = "TFL"
p_name  = "_TFL"

with open ("__init__.py", encoding = "utf-8") as f :
    version = str \
        (ast.literal_eval (_version_re.search (f.read ()).group (1)))

packages   = [p_name] + list (".".join ((p_name, p)) for p in find_packages ())
Q          = fs_find.Filter
data_dirs  = fs_find.directories \
    ( ".", filter = fs_find.Filter (include = Q.IN ("-I18N", "locale")))
data_files = list \
    ( itertools.chain
        ( ["LICENSE", "README.rst", "setup.py"]
        , fs_find.file_iter (".", filter = Q (include = Q.equal ("babel.cfg")))
        , fs_find.file_iter (* data_dirs)
        )
    )

class Test_Command (Command) :
    user_options = []

    def initialize_options (self) :
        pass

    def finalize_options (self) :
        pass

    def run (self) :
        import _TFL.run_doctest
        _TFL.run_doctest.Command (["-summary", "-transitive", "./"])

# end class Test_Command

if __name__ == "__main__" :
    setup \
    ( name                 = name
    , version              = version
    , description          =
        "Library with lots of useful stuff (says Ralf Schlatterbeck)"
    , long_description     =
        open ("README.rst", encoding = "utf-8").read ().strip ()
    , license              = license
    , author               = "Christian Tanzer"
    , author_email         = "tanzer@swing.co.at"
    , url                  = "https://github.com/Tapyr/tapyr"
    , packages             = packages
    , package_dir          = { p_name : "." }
    , package_data         = { p_name : data_files }
    , platforms            = 'Any'
    , classifiers          = \
        [ 'Development Status :: 5 - Production/Stable'
        , 'License :: OSI Approved :: ' + license
        , 'Operating System :: OS Independent'
        , 'Programming Language :: Python'
        , 'Programming Language :: Python :: 2'
        , 'Programming Language :: Python :: 2.7'
        , 'Programming Language :: Python :: 3'
        , 'Programming Language :: Python :: 3.5'
        , 'Intended Audience :: Developers'
        , 'Topic :: Software Development :: Libraries :: Python Modules'
        ]
    , install_requires     = []
    , extras_require       = dict
        ( bcrypt               = ["bcrypt"]
        , doc                  = ["plumbum", "sphinx"]
        , html_cleaner         = ["bs4"]
        , human_friendly_hsl   = ["husl"]
        , I18N                 = ["babel"]
        , timezone_support     = ["python-dateutil"]
        )
    , cmdclass             = dict (test = Test_Command)
    , zip_safe             = False ### no eggs, please
    )
