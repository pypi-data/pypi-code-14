
import numpy as np
import pylab as pl

import c5.config
import c5.sensors

PATH = '/home/alex/C5/vol_studies/'
speech_dir = PATH+'/datamining/audio'
brix_dir = PATH+'/datamining/brix'
marker_dir = PATH + '/datamining/marker_pos'
trial = 106
FRAMERATE = 20

MARKERS = [1,4,6,11,19,20,24,42,47,50,53,64,70,80,111,137,171,212,220]

#   1: balloon,       4: bbq,          6: birdsign, 11: bridge,
#  19: carpark,      20: fishsign,    24: hotel,    42: golf,
#  47: quadpark,     50: skater,      53: zoo,      64: hawk,
#  70: ropescourse,  80: playground, 111: compass  137: wasserschutz,
# 171: waterski,    212: train,      220: naturetrail

dt_speech = np.dtype({'names': ['timestamp','speech1','speech2','delta'], 
	'formats':['i8','i4','i4','i8']})

dt_array = [
('timestamp',np.uint64), ('speech1',np.uint16),
('speech2',np.uint16), ('speech_delta',np.uint64),
('brix1_gyrox', np.int), ('brix1_gyroy', np.int),
('brix1_gyroz', np.int), ('brix1_accx', np.int), 
('brix1_accy', np.int), ('brix1_accz', np.int), ('brix1_delta', np.uint64),
('brix2_gyrox', np.int), ('brix2_gyroy', np.int),
('brix2_gyroz', np.int), ('brix2_accx', np.int), 
('brix2_accy', np.int), ('brix2_accz', np.int), ('brix2_delta', np.uint64)
]

for i in MARKERS: 
	base = "m%i_" % (i) 
	dt_array.extend([
	(base+"hmd1_px",np.float), (base+"hmd1_py",np.float), (base+"hmd1_pz",np.float),
	(base+"hmd1_ow",np.float),
	(base+"hmd1_ox",np.float), (base+"hmd1_oy",np.float), (base+"hmd1_oz",np.float),
	(base+"hmd1_sx",np.int), (base+"hmd1_sy",np.int), (base+"hmd1_delta",np.uint64),
	(base+"hmd2_px",np.float), (base+"hmd2_py",np.float), (base+"hmd2_pz",np.float),
	(base+"hmd2_ow",np.float),
	(base+"hmd2_ox",np.float), (base+"hmd2_oy",np.float), (base+"hmd2_oz",np.float),
	(base+"hmd2_sx",np.int), (base+"hmd2_sy",np.int), (base+"hmd2_delta",np.uint64),
	(base+"top_px",np.float), (base+"top_py",np.float), (base+"top_pz",np.float),
	(base+"top_ow",np.float),
	(base+"top_ox",np.float), (base+"top_oy",np.float), (base+"top_oz",np.float),
	(base+"top_sx",np.int), (base+"top_sy",np.int),(base+"top_delta",np.uint64)
	])
	
data_type = np.dtype(dt_array)

config = c5.config.ConfigLoader(PATH+'trials.csv')
start = int(config.get(trial, config.CAM3_START))

# dont know where to stop exactly so i just use 43 minutes
stop = start + (43 * 60 * 1000)

trial_path = PATH + config.get(trial, config.DIRECTORY) + "/"
file_name = "%s/trial%d_speechrate.csv" % (speech_dir, trial)
speech = np.loadtxt(file_name, dtype=dt_speech, delimiter=',')

trial_path = PATH + config.get(trial, config.DIRECTORY) + "/"
in_file1 = trial_path + config.get(trial, config.BRIX1_LOG)
in_file2 = trial_path + config.get(trial, config.BRIX2_LOG)
brix1 = c5.sensors.load_brix_log(in_file1)
brix2 = c5.sensors.load_brix_log(in_file2)
err1 = np.loadtxt("%s/outlier_trial%d_brix1.csv" % (brix_dir, trial), delimiter = ',', dtype='i4')
err2 = np.loadtxt("%s/outlier_trial%d_brix2.csv" % (brix_dir, trial), delimiter = ',', dtype='i4')
err1 = np.unique(err1[:,1])
err2 = np.unique(err2[:,1])
brix1 = np.delete(brix1,err1, axis=0)
brix2 = np.delete(brix2,err2, axis=0)

del err1, err2

brix1 = c5.sensors.create_slots(start, stop, FRAMERATE, brix1)
brix2 = c5.sensors.create_slots(start, stop, FRAMERATE, brix2)

d = {}
for s in speech:
	t = int(s['timestamp'])
	if d.has_key(t) is False:
		d[t] = np.zeros((1,), dtype=data_type)
		d[t]['timestamp'] = t
		for typ in data_type.names:
			if "delta" in typ:
				d[t][typ] = -1
	a = d[t]
	a['speech1'] = s['speech1']
	a['speech2'] = s['speech2']
	a['speech_delta'] = s['delta']
	
for s in brix1:
	t = int(s['timestamp'])
	if d.has_key(t) is False:
		d[t] = np.zeros((1,), dtype=data_type)
		d[t]['timestamp'] = t
		for typ in data_type.names:
			if "delta" in typ:
				d[t][typ] = -1
	a = d[t]
	a['brix1_gyrox'] = s['gyrox']
	a['brix1_gyroy'] = s['gyroy']
	a['brix1_gyroz'] = s['gyroz']
	a['brix1_accx'] = s['accx']
	a['brix1_accy'] = s['accy']
	a['brix1_accz'] = s['accz']
	a['brix1_delta'] = s['delta']
	
for s in brix2:
	t = int(s['timestamp'])
	if d.has_key(t) is False:
		d[t] = np.zeros((1,), dtype=data_type)
		d[t]['timestamp'] = t
		for typ in data_type.names:
			if "delta" in typ:
				d[t][typ] = -1
	a = d[t]
	a['brix2_gyrox'] = s['gyrox']
	a['brix2_gyroy'] = s['gyroy']
	a['brix2_gyroz'] = s['gyroz']
	a['brix2_accx'] = s['accx']
	a['brix2_accy'] = s['accy']
	a['brix2_accz'] = s['accz']
	a['brix2_delta'] = s['delta']

#MARKERS=[24]
for i in MARKERS: 
	base = "m%i_" % (i)
	m = np.loadtxt(marker_dir+"/trial%i_%i.csv" % (trial,i), delimiter=',')
	for s in m:
		t = int(s[0])
		if d.has_key(t) is False:
			d[t] = np.nan((1,), dtype=data_type)
			d[t]['timestamp'] = t
			for typ in data_type.names:
				if "delta" in typ:
					d[t][typ] = -1
		a = d[t]	
		a[base + 'hmd1_delta'] = s[1]
		a[base + 'hmd1_px'] = s[2]
		a[base + 'hmd1_py'] = s[3]
		a[base + 'hmd1_pz'] = s[4]
		a[base + 'hmd1_ow'] = s[5]
		a[base + 'hmd1_ox'] = s[6]
		a[base + 'hmd1_oy'] = s[7]
		a[base + 'hmd1_oz'] = s[8]
		a[base + 'hmd1_sx'] = s[9]
		a[base + 'hmd1_sy'] = s[10]
		a[base + 'hmd2_delta'] = s[11]
		a[base + 'hmd2_px'] = s[12]
		a[base + 'hmd2_py'] = s[13]
		a[base + 'hmd2_pz'] = s[14]
		a[base + 'hmd2_ow'] = s[15]
		a[base + 'hmd2_ox'] = s[16]
		a[base + 'hmd2_oy'] = s[17]
		a[base + 'hmd2_oz'] = s[18]
		a[base + 'hmd2_sx'] = s[19]
		a[base + 'hmd2_sy'] = s[20]
		a[base + 'top_delta'] = s[21]
		a[base + 'top_px'] = s[22]
		a[base + 'top_py'] = s[23]
		a[base + 'top_pz'] = s[24]
		a[base + 'top_ow'] = s[25]
		a[base + 'top_ox'] = s[26]
		a[base + 'top_oy'] = s[27]
		a[base + 'top_oz'] = s[28]
		a[base + 'top_sx'] = s[29]
		a[base + 'top_sy'] = s[30]

arr = np.array(d.values(), dtype=data_type)
arr.sort(axis=0,order='timestamp')
pl.plot(arr['speech1'])
del d
np.save("full_data.npy", arr)                                                                                                                                                                                                                                           

