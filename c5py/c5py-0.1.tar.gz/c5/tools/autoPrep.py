# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-

import numpy as np
import pylab as pl
import sys
import os
sys.path.append(os.path.abspath('../../'))
import c5.sensors

### this script assists in finding outliers. it presents a feature dimension
### and allows marking these in a plot. the marked positions are saved in a 
### file (including the dimension it was marked in) and can be used to remove
### these data from the data set.

#f = "/home/alex/C5/vol_studies/2011-12_ARBaseline/20111213_0900/BRIX_s2_2011-12-13 09:10:25.750399.log"

f = sys.argv[1]
out = sys.argv[2]

idx = 0

d1 = c5.sensors.load_brix_log(f)

if os.path.exists(out) is True:
	print "warning! file already exist"
	sys.exit(1);
	
delete = []
l = ['gyrox','gyroy','gyroz','accx','accy','accz']

for idx in range(6):
	last_idy = 0	
	y = d1[:][l[idx]]
	dy = np.abs(np.diff(y))
	for idy in range(4,dy.shape[0]):
		p = dy[idy-4:idy]
		if (np.abs(p[0]-p[3]) < 20) and (np.abs(p[1] - p[2]) < 20) and (np.abs(p[1] - p[0]) > 200):
			if idy-2-last_idy > 1: 
				delete.append((idx,idy-2))
				last_idy = idy
			
def detect(y):
	dy = np.abs(np.diff(y))
	res = [0]
	for idy in range(4,dy.shape[0]):
		p = dy[idy-4:idy]
		if (np.abs(p[0]-p[3]) < 20) and (np.abs(p[1] - p[2]) < 20) and (np.abs(p[1] - p[0]) > 200):
			if (idy - res[-1] > 1):			
				res.append(idy-2)
	res.pop(0)
	pl.plot(y)
	pl.plot(dy)
	pl.plot(res, np.zeros(len(res)), 'rx')
		
	
r = np.array(delete)
np.savetxt(out, r, delimiter=',')
