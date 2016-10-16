#!/usr/bin/env python
# encoding: utf-8

"""
This module of predefinitions is implemented to expose
certain preprocessor #defines that can be used in an 010
template script to determine if it is being run under pfp
or in the actual 010 editor.
"""

import pfp
from pfp.native import native, predefine


predefine("""
#define PFP
#define PFP_VERSION "{version}"
""".format(
    version = pfp.__version__
))
