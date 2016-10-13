#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2016 Mag. Christian Tanzer. All rights reserved
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
#    _CHJ.setup
#
# Purpose
#    Setup file for package namespace CHJ
#
# Revision Dates
#    11-Oct-2016 (CT) Creation
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

name    = "CHJ"
p_name  = "_CHJ"

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
        "Package for CSS/HTML/Javascript support."
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
    , setup_requires       = ["TFL"]
    , install_requires     = ["TFL"]
    , extras_require       = dict
        ( minified             = ["rcssmin", "rjsmin"]
        , minified_debian_slow = ["cssmin",  "jsmin"]
            ### cssmin and jsmin are available as debian packages but almost an
            ### order of magnitude slower than rcssmin and rjsmin
            ### * for development, you don't want that
            ### * for deployment, it shouldn't matter much as they are used
            ###   only once during deployment
        )
    , cmdclass             = dict (test = Test_Command)
    , zip_safe             = False ### no eggs, please
    )
