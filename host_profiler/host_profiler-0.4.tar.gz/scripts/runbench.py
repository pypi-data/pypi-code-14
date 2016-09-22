#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from host_profiler.bench import Bench
from host_profiler.benchproc import benchproc

if __name__ == '__main__':
    p = []
    f = ''
    a = False
    b = False
    for v in sys.argv:
        if a:
            if not v.startswith('-'):
                p.append(v)
            else:
                a = False
        if b:
            f = v
            b = False
        if v == '-p':
            a = True
        if v == '-f':
            b = True

    if f == '':
        #print('error usage: runbench -f result_folder (-p processus_to_bench)')
        print('error usage: runbench.py -f result_folder')

    if len(p) == 0:
        Bench(f)
    else:
        for i in  p:
            benchproc(f, i)

