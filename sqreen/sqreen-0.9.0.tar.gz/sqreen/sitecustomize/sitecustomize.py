# -*- coding: utf-8 -*-
# Copyright (c) 2016 Sqreen. All Rights Reserved.
# Please refer to our terms for more information: https://www.sqreen.io/terms.html
""" Module called when sitecustomize is automatically imported by python
"""
import sys
from sqreen import start

# Try to detect when this module is imported as sitecustomize
if not hasattr(sys, 'argv'):
    start()
