#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    COPYRIGHT (C) 2016 by Sebastian Stigler

    NAME
        run_commandline.py -- Testprogramm for RunCode class

    FIRST RELEASE
        2016-07-05  Sebastian Stigler  sebastian.stigler@hs-aalen.de

"""
import sys

print(sys.argv[1])
sys.stdout.flush()
print(sys.argv[2], file=sys.stderr)
sys.stderr.flush()

sys.exit(4)
# vim: ft=python ts=4 sta sw=4 et ai
