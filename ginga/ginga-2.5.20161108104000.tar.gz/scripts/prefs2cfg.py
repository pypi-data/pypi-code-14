from __future__ import print_function
#! /usr/bin/env python
#
import sys, os
import logging
from ginga.misc import Settings

LOG_FORMAT = '%(asctime)s | %(levelname)1.1s | %(filename)s:%(lineno)d (%(funcName)s) | %(message)s'

path = sys.argv[1]
dirpath, file = os.path.split(path)
name, ext = os.path.splitext(file)

logger = logging.getLogger("devnull")
stderrHdlr = logging.StreamHandler()
stderrHdlr.setLevel(logging.DEBUG)
stderrHdlr.setFormatter(LOG_FORMAT)
logger.addHandler(stderrHdlr)

prefs = Settings.Preferences(basefolder=dirpath, logger=logger)

with open(path, 'r') as in_f:
    buf = in_f.read()

d = eval(buf)

cat = prefs.createCategory(name)
cat.setDict(d)
cat.save()

print("DONE")
