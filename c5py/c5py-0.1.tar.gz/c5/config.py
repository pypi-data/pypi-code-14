# -*- coding: utf-8 -*-

import json
import collections
import numpy as np
import sys
import os.path 

SAMPLING_RATE = 50 # Hz 
SAMPLING_INTERVAL = 1000 / SAMPLING_RATE # ms


# Names
VOL_PATH = os.environ["C5_VOL_PATH"] if "C5_VOL_PATH" in os.environ else '.'
RAW_PATH = os.environ["C5_RAW_PATH"] if "C5_RAW_PATH" in os.environ else '.'
DATA_PATH = os.environ["C5_DATA_PATH"] if "C5_DATA_PATH" in os.environ else '.'

MARKER_DT = np.dtype({
    'names': ['timestamp', 'id', 'p_x', 'p_y', 'p_z',
              'o_w', 'o_x', 'o_y', 'o_z', 's_x', 's_y'],
    'formats': [np.uint64, np.uint, np.float, np.float, np.float,
                np.float, np.float, np.float, np.float, np.float, np.float]})

MARKER_IDS = [1,4,6,11,19,20,24,42,47,50,53,64,70,80,111,137,171,212,220]
MARKER_ACRONYMS = { 1: "HAB", 4: "BBQ", 6: "QP", 11: "BR", 19: "CP", 20: "MG", 
                    24: "WPA", 42: "FS", 47: "BD", 50: "SP", 53: "PZ", 64: "NPA", 70: "RC",
                    80: "WP", 111: "Compass", 137: "H", 171: "WS", 212: "KT", 220: "NT"}

BRIX_DT = np.dtype({'names': ['timestamp','gyrox','gyroy','gyroz','accx','accy','accz'],
            'formats':['i8','i4','i4','i4','i4','i4','i4']})

MARKER_DELTA_DT = np.dtype(MARKER_DT.descr +
                     np.dtype([('delta', np.uint64)]).descr)
BRIX_DELTA_DT = np.dtype(BRIX_DT.descr +
                     np.dtype([('delta', np.uint64)]).descr)
                     
DTYPE_DEFAULTS = {np.dtype('uint64'):np.nan, np.dtype('<U22'):'', np.dtype('float64'):np.nan}

STUDIES = ['2011-12_ARBaseline', '2012-04_NoARBaseline', '2013-04_ARPre',
           '2013-07_ARAssistance', '2014-04_ARInterception']

SYNC_XML = {}
SYNC_XML['2011-12_ARBaseline'] = "c5_AR.xml"
SYNC_XML['2012-04_NoARBaseline'] = "c5_NoAR.xml"
SYNC_XML['2013-04_ARPre'] = "c5_ExtAR.xml"
SYNC_XML['2013-07_ARAssistance'] = "c5_ARAss.xml"
SYNC_XML['2014-04_ARInterception'] = "c5_AREnh.xml"

TRIALS = {}
TRIALS['2011-12_ARBaseline'] = range(101, 111)
TRIALS['2012-04_NoARBaseline'] = range(201, 213)
TRIALS['2013-04_ARPre'] = range(301, 306)
TRIALS['2013-07_ARAssistance'] = range(401, 416)
TRIALS['2014-04_ARInterception'] = range(501, 516)

# raw
RAW_NAMES={}
RAW_NAMES['config_json'] = "trial%d.json"
RAW_NAMES['video_ogv_hmd1'] = "trial%d_hmd1.ogv"
RAW_NAMES['video_ogv_hmd2'] = "trial%d_hmd2.ogv"
RAW_NAMES['video_dv_cam1'] = "VP_Gruppe_%d/cam_1/AVCHD"
RAW_NAMES['video_dv_cam2'] = "VP_Gruppe_%d/cam_2/AVCHD"
RAW_NAMES['video_dv_cam3'] = "VP_Gruppe_%d/cam_3/AVCHD"
RAW_NAMES['brix_s1'] = "trial%d_brix_s1.log"
RAW_NAMES['brix_s2'] = "trial%d_brix_s2.log"
RAW_NAMES['brix_sync'] = "trial%d_sync1.log"
RAW_NAMES['tracker_hmd'] = "trial%d_hmd.xml"
RAW_NAMES['tracker_top'] = "trial%d_cam3.xml"
RAW_NAMES['kinect_old'] = "trial%d_kinect.zlib"
RAW_NAMES['kinect_new'] = "trial%d_kinect.c5k"
RAW_NAMES['mic_wav'] = "trial%d_mic.wav"

# preprocessed
FILE_NAMES={}
FILE_NAMES['video_cam1'] = "trial%d_cam1.mp4"
FILE_NAMES['video_cam2'] = "trial%d_cam2.mp4"
FILE_NAMES['video_cam3'] = "trial%d_cam3.mp4"
#FILE_NAMES['video_mp4_hmd1'] = "trial%d_hmd1.mp4" // hmd videos are not included because of their wrong timing
#FILE_NAMES['video_mp4_hmd2'] = "trial%d_hmd2.mp4" // if required, they should be cropped from the merged video
FILE_NAMES['video_all'] = "Trial%02d.mp4"
FILE_NAMES['config_json'] = "trial%d.json"
FILE_NAMES['ca_deixis'] = "Trial%02d_dG.eaf"
FILE_NAMES['ca_time'] = "Trial%02d_zE.eaf"
FILE_NAMES['ca_gaze'] = "Trial%02d_MutualGaze.eaf"
FILE_NAMES['ca_full'] = "Trial%02d_final.eaf"
FILE_NAMES['tracker_hmd1'] = "trial%d_artkp_hmd1.csv"
FILE_NAMES['tracker_hmd2'] = "trial%d_artkp_hmd2.csv"
FILE_NAMES['tracker_cam3'] = "trial%d_artkp_cam3.csv"
FILE_NAMES['brix_s1'] = "trial%d_brix_s1.csv"
FILE_NAMES['brix_s2'] = "trial%d_brix_s2.csv"
FILE_NAMES['kinect_free'] = "trial%d_kinect_free.zip"
FILE_NAMES['kinect_nego'] = "trial%d_kinect_negotiation.zip"
FILE_NAMES['kinect_pres'] = "trial%d_kinect_presentation.zip"
FILE_NAMES['mic_wav'] = "trial%d_mic.wav"


class ConfigLoader():
    #DIRECTORY = 1;    MERGED_VIDEO = 2
    #CAM1_VIDEO = 3;    CAM1_START = 4;    CAM2_VIDEO = 5;    CAM2_START = 6
    #CAM3_VIDEO = 7;    CAM3_START = 8;    HMD1_VIDEO = 9; HMD2_VIDEO = 11;
    #MIC = 13;

    def __init__(self, filename=None, path=None):
        self._data = {}
        path = VOL_PATH if path is None else path
        if isinstance(filename, int):
            fname = FILE_NAMES['config_json'] % filename
            filename = "%s/%s/trial%d/%s" % (path, STUDIES[filename/100-1],
                                             filename, fname)
        if filename is not None:
            self.load(filename)

    def load(self, filename):
        with open(filename, 'r') as f:
            self._data = json.load(f)

    def data(self):
        return self._data

    def has_element(self, path):
        return self._step_down((self._data), path.split('.')) is not None

    def get(self, path):
        return self._step_down(self._data, path.split('.'))

    def set(self, path, value):
        return self._step_down(self._data, path.split('.'), value)

    def save(self, filename, overwrite=False):
        if os.path.exists(filename) and not overwrite:
            print "file exists"
            return False
        with open(filename, 'w') as f:
            json.dump(self._data, f, indent=4, sort_keys=True)
            return True

    def _step_down(self, elem, path, value=None):
        if isinstance(elem, collections.Iterable):
            if len(path) > 1:
                key = path.pop(0)
                if key in elem:
                    return self._step_down(elem[key], path, value)
                elif value is not None:
                    elem[key] = {}
                    return self._step_down(elem[key], path, value)
            elif len(path) == 1:
                key = path.pop(0)
                if value is not None:
                    elem[key] = value
                return elem[key]
        return None

def get_config(timestamp, trial=None):
    conf = None
    if trial is not None:
        return ConfigLoader(trial), trial
    for study in STUDIES:
        for tid in TRIALS[study]:
            conf = ConfigLoader(tid)
            if conf.get('trial.stop') > timestamp:
                return conf, tid
    return None, None


def main(argv=None):
    if argv is None:
        argv = sys.argv
    if not os.path.exists(argv[1]):
        print "%s does not exist" % argv[1]
        return
    loader = ConfigLoader(argv[1])
    if (loader.has_element("hmd1.start")):
        loader.set("hmd1.test", 1337)
        loader.set("hmd1.test2", "teststring")
        loader.set("hmd1.start.test", 1)
        print loader.get("hmd1.start")
        print loader.get("hmd1.test")
        print loader.get("hmd1.test2")
        print loader.get("hmd1.start.test")
    else:
        print "path not found"


if __name__ == "__main__":
    sys.exit(main())
