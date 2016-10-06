#!/usr/bin/env python2

from __future__ import print_function
from __future__ import division

import sys
import os
import time

sys.path.append('../extras/pystarlib/pystarlib/src')
from STAR import File


d = os.path.abspath(sys.argv[1])
print("Reading from %s.  "%(d),end='')


filenames = [os.path.join(d,f) for f in os.listdir(d)]
print("Found %d files."%(len(filenames)))

ta = time.time()
print("START:\r\t\t", ta)

for i, f in enumerate(filenames):
    fta = time.time()
    try:
        sf = File.File(filename=f)
        sf.read()
        ftb = time.time()
        print("OKAY\t" + os.path.basename(f) + "\t", ftb - fta, "\t", i)
    except KeyboardInterrupt:
        exit()
    except:
        ftb = time.time()
        print("FAIL\t" + os.path.basename(f) + "\t", ftb - fta, "\t", i)

tb = time.time()
print("END:\r\t\t", tb)
print("Files read in %s seconds"%(tb-ta))
