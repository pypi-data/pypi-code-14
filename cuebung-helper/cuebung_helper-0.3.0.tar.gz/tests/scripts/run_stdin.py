#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    COPYRIGHT (C) 2016 by Sebastian Stigler

    NAME
        run_stdin.py -- Testprogramm for RunCode class

    FIRST RELEASE
        2016-07-05  Sebastian Stigler  sebastian.stigler@hs-aalen.de

"""
import sys

VAL = input()  # expact "val1 val2"

SPVAL = VAL.split(" ")

print(SPVAL[0])
sys.stdout.flush()
print(SPVAL[1], file=sys.stderr)
sys.stderr.flush()

sys.exit(3)
# vim: ft=python ts=4 sta sw=4 et ai
