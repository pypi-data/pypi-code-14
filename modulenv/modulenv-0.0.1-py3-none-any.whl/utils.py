# utils.py
#
# part of modulenv
#
# Copyright (c) 2016 Sven E. Templer
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy of this
# software and associated documentation files (the "Software"), to deal in the Software
# without restriction, including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons
# to whom the Software is furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all copies or
# substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
# PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE
# FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

import os
import sys
import time
import re

def quit ( msg, 
           code = 65 ):
    msg = 'error: ' + msg
    print(msg)
    sys.exit(code)

def warn ( msg ):
    msg = 'warning: ' + msg
    print(msg)

def log ( msg, path = 'log' ):
    now = time.strftime('%Y-%m-%d %H:%M:%S')
    msg = '[' + now + '] ' + msg + '\n'
    f = open(path, 'a')
    f.write(msg)
    f.close()

def grep ( path = None, pattern = None, replacement = None, lines = None ):
    p = []
    if path:
        f = open(path, 'r')
        lines = [ line for line in f.readlines() ]
        f.close()
    elif not lines:
        quit('need path or lines')
    if not pattern:
        return p
    for line in lines:
        if re.search(pattern, line):
            line = line.rstrip()
            if replacement is not None:
                line = re.sub(pattern, replacement, line)
            p.append(line)
    return p

def pathnorm ( path ):
    path = os.path.expanduser(path)
    path = os.path.realpath(path)
    return path

def pathdepth ( path, sep = os.path.sep):
    path = pathnorm (path)
    return len(path.split(sep)) - 1

def pathtree ( path, level = 1, parent = False, absolute = False, 
               incdir = True, incfile = True ):
    path = pathnorm(path)
    depth0 = pathdepth(path)
    chars0 = len(path) + 1 # include trailing '/'
    w = os.walk(path)
    tree = []
    if not incdir and not incfile:
        return tree
    for p, d, f in w:
        inodes = []
        if incdir:
            inodes.extend(d)
        if incfile:
            inodes.extend(f)
        for i in inodes:
            i = os.path.join(p, i)
            depth = pathdepth(i)
            delta = depth - depth0
            if delta == level or (parent and delta < level):
                if not absolute:
                    i = i[chars0:]
                tree.append(i)
    return tree

def lsdir2 ( path ):
    dirs = []
    for prog in os.listdir(path):
        if not os.path.exists(path):
            for vers in os.listdir(path + '/' + prog):
                dirs.append(prog + '/' + vers)
    return dirs

#def scriptpath ( ):
#    p = os.path.realpath(__file__)
#    return p

def printdir2 ( path ):
    p = print_root
    d = lsdir2(path)    

def subdirstr ( ):
    return None

