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
#    _ReST.setup
#
# Purpose
#    Setup file for package namespace ReST
#
# Revision Dates
#    12-Oct-2016 (CT) Creation
#    ««revision-date»»···
#--

from   __future__               import print_function

from   codecs                   import open
from   setuptools               import setup, Command

import ast
import os
import re
import subprocess               as     SUBP
import sys

_version_re = re.compile(r'__version__\s+=\s+(.*)')

src_dir = os.path.dirname (__file__)
if src_dir :
    os.chdir (src_dir)

license = "BSD License"

name    = "ReST-Tapyr"
p_name  = "_ReST"

with open ("__init__.py", encoding = "utf-8") as f :
    version = str \
        (ast.literal_eval (_version_re.search (f.read ()).group (1)))

packages = []
for root, dirs, files in os.walk (os.path.join ('..', p_name)) :
    # ugly: need to modify dirs in place!
    dd = set (d for d in dirs if d.startswith ('_') and d != "__pycache__")
    for d in dirs :
        if d not in dd :
            dirs.remove (d)
    packages.append (root.replace ('/', '.').strip ("."))

data_files = ["LICENSE", "README.rst"]
with SUBP.Popen \
    (["find", ".", "-name", "babel.cfg"], stdout=SUBP.PIPE).stdout as pipe :
    found = pipe.read ().strip ()
    if found :
        bcs = found.split ("\n")
        data_files.extend (bcs)

data_dirs  = []
with SUBP.Popen \
    (["find", ".", "-name", "-I18N"], stdout=SUBP.PIPE).stdout as pipe :
    found = pipe.read ().strip ()
    if found :
        i18n_dirs = found.split ("\n")
        data_dirs.extend (i18n_dirs)
for d in data_dirs :
    with SUBP.Popen \
        (["find", d, "-type", "f"], stdout=SUBP.PIPE).stdout as pipe :
        found = pipe.read ().strip ()
        if found :
            files = found.split ("\n")
            data_files.extend (files)

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

setup \
    ( name                 = name
    , version              = version
    , description          =
        "Package augmenting docutil's reStructuredText handling."
    , long_description     =
        open ("README.rst", encoding = "utf-8").read ().strip ()
    , license              = license
    , author               = "Christian Tanzer"
    , author_email         = "tanzer@swing.co.at"
    , url                  = "https://github.com/Tapyr/tapyr"
    , packages             = packages
    , package_dir          = { p_name : "../" + p_name }
    , package_data         = { p_name : data_files     }
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
    , install_requires     = ["TFL", "docutils"]
    , extras_require           = dict ()
    , cmdclass             = dict (test = Test_Command)
    , zip_safe             = False ### no eggs, please
    )
