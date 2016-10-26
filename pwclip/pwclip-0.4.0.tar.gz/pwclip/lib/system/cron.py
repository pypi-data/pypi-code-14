
import os
import re

from os import \
    stat as _stat, \
    remove as _remove

from datetime import \
    datetime as _datetime

def stamp():
	now = _datetime.now()
	stamp = '%s.%s'%(now.date(), str(now.time()).split('.')[0])
	return stamp

def fileage(trgfile):
	timefile = '/tmp/thetime'
	trgtime = _stat(trgfile).st_mtime
	with open(timefile, 'w+'):
		thetime = _stat(timefile).st_mtime
	os.remove(timefile)
	return int(str(((thetime-trgtime))).split('.')[0])

