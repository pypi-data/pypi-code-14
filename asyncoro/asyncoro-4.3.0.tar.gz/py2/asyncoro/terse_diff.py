#!/usr/bin/env python

from __future__ import print_function
import sys

prev_line = '>'
for line in sys.stdin:
    if line[0] == '<':
        if prev_line[0] == '>':
            print('---\n%s' % line, end='')
        else:
            print(line, end='')
        prev_line = line
    elif line[0] == '>':
        print(line, end='')
        prev_line = line
        
