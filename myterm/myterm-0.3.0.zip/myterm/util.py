#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    module myterm.util
"""
def first_value(*args):
    for arg in args:
        if arg != None and arg != '':
            return arg
    return args[-1]
