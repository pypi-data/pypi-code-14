#!/usr/bin/python
#Last-modified: 05 May 2016 02:47:08 PM

#         Module/Scripts Description
# 
# Copyright (c) 2008 Yunfei Wang <tszn1984@gmail.com>
# 
# This code is free software; you can redistribute it and/or modify it
# under the terms of the BSD License (see the file COPYING included with
# the distribution).
# 
# @status:  experimental
# @version: 1.0.0
# @author:  Yunfei Wang
# @contact: tszn1984@gmail.com

# ------------------------------------
# python modules
# ------------------------------------

import sys
import string
from ngslib import IO

# ------------------------------------
# constants
# ------------------------------------

# ------------------------------------
# Misc functions
# ------------------------------------

# ------------------------------------
# Classes
# ------------------------------------

# ------------------------------------
# Main
# ------------------------------------

if __name__=="__main__":
    if len(sys.argv)==1:
        sys.exit("Example:"+sys.argv[0]+" anno.tab/bed\n\tPrint TSS position in Bed format.")
    for item in IO.BioReader(sys.argv[1],ftype= 'guess'):
        print item.getTSS()

