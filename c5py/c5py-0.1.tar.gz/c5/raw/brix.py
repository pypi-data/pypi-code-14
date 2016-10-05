# -*- coding: utf-8 -*-
"""
Created on Fri Mar  7 18:38:03 2014

@author: alneuman
"""

import os.path
import sys
if __name__ == '__main__' and __package__ is None:
    new_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.append(new_path+"/../")

import struct
import numpy as np
import c5.config
from c5.config import TRIALS
import c5.data
import c5.sensors
import os

def check(path, trial):
    cfg = os.path.exists("%s/trial%d.json" % (path, trial))
    b1 = os.path.exists("%s/trial%d_brix_s1.log" % (path, trial))
    b2 = os.path.exists("%s/trial%d_brix_s2.log" % (path, trial))
    return (cfg and b1 and b2)


def _benchmark_check(path, trial):
    out1 = os.path.exists("%s/brix_outlier1.log" % (path, trial))
    out2 = os.path.exists("%s/brix_outlier2.log" % (path, trial))
    return (check(path, trial) and out1 and out2)


def convert_data(path, trial, out="."):
    out1_path = "%s/trial%d_brix_s1.csv" % (out, trial)
    out2_path = "%s/trial%d_brix_s2.csv" % (out, trial)
    if os.path.exists(out1_path) or os.path.exists(out2_path):
        print "data for trial %d already exist. skip" % trial
        return

    #load brix data: already removes incomplete lines
    b1 = c5.sensors.load_brix_log("%s/trial%d_brix_s1.log" % (path, trial))
    b2 = c5.sensors.load_brix_log("%s/trial%d_brix_s2.log" % (path, trial))

    #brix got unix timestamps; no fix required
    o1 = detect_outlier(b1)
    o2 = detect_outlier(b2)

    b1_new = np.delete(b1, o1)
    b2_new = np.delete(b2, o2)

   # b1_out = c5.data.create_slots(start, stop, 1000/50, b1_new)
   # b2_out = c5.data.create_slots(start, stop, 1000/50, b2_new)

    head = ", ".join(c5.config.BRIX_DT.names)

    np.savetxt(out1_path, b1_new, "%d", ",",
               header=head)
    np.savetxt(out2_path, b2_new, "%d", ",",
               header=head)


def int2bit(value):
    # little endian short expected
    c = struct.pack("<h", value)
    lsb = struct.unpack("B", c[0])[0]
    hsb = struct.unpack("B", c[1])[0]
    return lsb, hsb


def detect_outlier(data, sensors=None, params=None):
    out = []
    if sensors is None:
        sensors = c5.config.BRIX_DT.names
    for key in sensors:
        if key == 'timestamp':
            continue
        arr = [int2bit(x) for x in data[key]]
        arr = np.array(arr)
        out_tmp = _detect_outlier_step(arr, params)
        out.extend(out_tmp)
    dt = data['timestamp'][1:] - data['timestamp'][:-1]
    out = np.unique(out)

    # condition 3: if too much time passed between two samples, remove marker
    res = []
    dt = np.where(dt > 200)[0]
    for idx in out:
        #print dt
        #print idx
        if (idx-1) not in dt:
            res.append(idx)
    return res


def _detect_outlier_step(data, params):
    if params is None:
        # retrieved by test run see Pre-Brix notebook
        params = {'msb_lag': 46, 'lsb_shift': 200, 'lsb_lag': 61, 'msb_shift': 128}
    # we check two conditions
    out1 = np.zeros(data.shape[0])
    out2 = np.zeros(data.shape[0])
    t_lsb = data[0, 0]
    t_hsb = data[0, 1]
    for i in range(0, data.shape[0]):
        c_lsb = data[i, 0]
        c_hsb = data[i, 1]
        
        abs_lsb = abs(t_lsb - c_lsb)
        abs_hsb = abs(t_hsb - c_hsb)
        # 1st condition: if there is a lsb drop without any hsb activity,
        # we assume ansynchronous reading
        if abs_hsb == 0:
            if abs_lsb > params['lsb_shift']:
                # to avoid double detection we only classify if
                # the preceeding frame wasnt classified
                if out1[i-1] + out2[i-1] == 0:
                    out1[i] = 1
        # 2nd condition: if there is change in the msb but almost none in lsb
        else:
            # 2a: msb shift indicates change of signs
            if abs_hsb > params['msb_shift']:
                if abs_lsb < params['lsb_lag']:
                    if out1[i-1] + out2[i-1] == 0:
                        out2[i] = 1
            # 2b: msb indicates significant value change
            else:
                if abs_lsb < params['msb_lag']:
                    if out1[i-1] + out2[i-1] == 0:
                        out2[i] = 1
        t_hsb = c_hsb
        t_lsb = c_lsb
    out = []
    # summarize outliers
    for i in range(0, data.shape[0]):
        if out1[i] + out2[i] > 0:
            out.append(i)
    return out


def main():
    for study, trials in TRIALS.items():
        for trial in trials:
            raw = "%s/%s/trial%d" % (os.environ['C5_RAW_PATH'], study, trial)
            vol = "%s/%s/trial%d" % (os.environ['C5_VOL_PATH'], study, trial)
            if check(raw, trial) is False:
                print "data missing. exit"
                return
            convert_data(raw, trial, vol)

if __name__ == "__main__":
    sys.exit(main())