# -*- coding: utf-8 -*-
"""
Created on Fri Mar  7 18:38:03 2014

@author: alneuman
"""

import sys
import os.path
import tempfile
import xml.sax as sax
import struct
import numpy as np
import cv2

from ..config import TRIALS, STUDIES, MARKER_DT, RAW_PATH, VOL_PATH, ConfigLoader
from .. import data

VELO_THRESHOLD = 1

HMD_MATRIX = np.matrix([[3.24861, 0, 0, 0],
                        [0, 4.33148, 0, 0],
                        [0, 0, -1.00002, 1.00136e-05],
                        [0, 0, -1, 1]])


def check(path, trial):
    cfg = os.path.exists("%s/trial%d.json" % (path, trial))
    hmd = os.path.exists("%s/trial%d_hmd.xml" % (path, trial))
    cam = os.path.exists("%s/trial%d_cam3.xml" % (path, trial))
    return (cfg and hmd and cam)


def filter_data(data, threshold, limit=3):
    mids = np.unique(data['id'])
    cleared = np.copy(data)
    for mid in mids:
        d = data[np.where(data['id'] == mid)]
        if d.shape[0] > 0:
            count = 0
            drops = np.zeros(1)
            res = np.copy(d)
            fres = []
            while count != limit and drops.shape[0] > 0:
                foc = (cleared['id'] == mid)
                d = cleared[foc]
                dx = (d['s_x'][1:]-d['s_x'][:-1]) / (d['timestamp'][1:]-d['timestamp'][:-1])
                dx = abs(dx)
                dy = (d['s_y'][1:]-d['s_y'][:-1]) / (d['timestamp'][1:]-d['timestamp'][:-1])
                dy = abs(dx)
                drops = np.where((dx > threshold) | (dy > threshold))[0]
                d['id'][drops] = 0
                cleared[foc] = d
                count += 1

    clear_idx = np.where(cleared['id'] == 0)
    cleared = np.delete(cleared, clear_idx)
    return cleared, clear_idx[0].shape[0]


class RegionExtractor():
    def __init__(self):
        import cv2
        self.points = [(0, 0), (1920, 1080)]
        self.idx = 0
        self.img = None

    def mouse_up(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONUP:
            print "%d:%d" % (x, y)
            if y < 10:
                y = 0
            elif y > 1070:
                y = 1080
            self.points[self.idx] = (x, y)
            img2 = self.img.copy()
            cv2.rectangle(img2, self.points[0], self.points[1], (0, 255, 0), 3)
            cv2.imshow('image', img2)

    def extract(self, path):
        cap = cv2.VideoCapture(path)
        if cap.isOpened():
            ret, self.img = cap.read()
        else:
            print "ERROR: no video at %s" % path
        cap.release()
        cv2.imshow('image', self.img)
        cv2.setMouseCallback('image', self.mouse_up)
        while(1):
            k = cv2.waitKey(1) & 0xFF
            if k == ord('m'):
                self.idx += 1
            if k == ord('n'):
                self.idx -= 1
            # we ignore the inner rectangle, otherwise 1 should be 3
            elif k == 27 or self.idx > 1:
                break
        cv2.destroyWindow('image')
        return self.points


def load_xcf_log(filename, time=None, matrix=None, res_x=None, res_y=None):
    if os.path.exists(filename) is False:
        return None
    tmp_fd, tmp_path = tempfile.mkstemp()
    tmp_file = open(tmp_path, 'w')
    tmp_file.write("<LAFORGE>\n")
    last_line = ''
    with open(filename, 'r') as f:
        for line in f:
            if line.startswith('<MARKER'):
                tmp_file.write(last_line)
                last_line = line
    tmp_file.write("</LAFORGE>\n")
    tmp_file.close()
    handler = XcfHandler(time, matrix, res_x, res_y)
    parser = sax.make_parser()
    parser.setContentHandler(handler)
    parser.parse(tmp_path)
    data = handler.result()
    res = {}
    for key, value in data.items():
        if '/' in key:
            key = key.split('/')[-2]
            key += "_artkp"
            if "trial" in key:
                key = "cam3_artkp"
        res[key] = np.array(value, dtype=MARKER_DT)
    return res


class XcfHandler(sax.handler.ContentHandler):
    def __init__(self, time=None, matrix=None, res_x=None, res_y=None):
        self.time_cue = struct.pack("L", time)[4:] if time is not None else None
        self.timeframe = {}
        self.active = None
        self.timestamp = None
        self.generator = None
        self.matrix = matrix
        self.res_x = res_x
        self.res_y = res_y
        self._result = {}
        # ignore origin parameters
        self.is_origin = False

    def startElement(self, name, attrs):
        if name == "UPDATED":
            value = attrs["value"]
            # bugfix:
            # some versions of the position_logger have a bug where the uint64
            # timestamp is broken and only the first 4 byte are written.
            # Luckily these false timestamps can be identified by the suffix
            # which is 'll'. To repair these values we require a valid uint64
            # timestamp from the trial. Any value from the configuration or the
            # sync event should be valid.
            if 'll' in value:
                if time.time_cue is None:
                    raise Error("Broken timestamp detected but no time cue was passed.")
                value = struct.pack('I', int(value[:-2])) + self.time_cue
                value = struct.unpack('L', value)[0]
                #print value
            self.timestamp = value
        elif name == "GENERATOR":
            self.generator = ""
        elif name == "MARKERCOORDINATES":
            # new coordinates, delete old data except timestamp
            m_data = ['p_x', 'p_y', 'p_z', 'o_w', 'o_x', 'o_y', 'o_z',
                      's_x', 's_y']
            for k in m_data:
                if k in self.timeframe:
                    self.timeframe.pop(k)
            self.timeframe = {}
            self.timeframe['id'] = attrs['id']
        elif name == "POINT3D" and self.is_origin is False:
            self.timeframe['p_x'] = attrs['x']
            self.timeframe['p_y'] = attrs['y']
            self.timeframe['p_z'] = attrs['z']
            if self.matrix is not None:
                pos = np.array([float(attrs['x']), float(attrs['y']),
                                float(attrs['z']), 1])
                #@TODO: this needs to be extracted from the call
                screen = self.convertSceneToScreenPosition(
                    pos, self.matrix, self.res_x, self.res_y)
                self.timeframe['s_x'] = screen[0]
                self.timeframe['s_y'] = screen[1]
        elif name == "POINT2D" and self.is_origin is False and self.matrix is None:
            self.timeframe['s_x'] = float(attrs['x'])
            self.timeframe['s_y'] = float(attrs['y'])
        elif name == "QUATERNION" and self.is_origin is False:
            self.timeframe['o_w'] = attrs['w']
            self.timeframe['o_x'] = attrs['x']
            self.timeframe['o_y'] = attrs['y']
            self.timeframe['o_z'] = attrs['z']
        elif name == "ORIGIN":
            self.is_origin = True
        self.active = name

    def characters(self, content):
        if self.active == "GENERATOR":
            self.generator += content

    def endElement(self, name):
        if name == "MARKERCOORDINATES":
            # skip invalid data
            # we know the data is invalid since 0 is the point of origin
            if self.timeframe['p_x'] == 0:
                return
            self.timeframe['timestamp'] = self.timestamp
            # Normalize Data if the resolution was supplied
            if self.res_x is not None:
                self.timeframe['s_x'] /= self.res_x
                self.timeframe['s_y'] /= self.res_y
            row = []
            for field in MARKER_DT.names:
                row.append(self.timeframe[field])
            self._result.setdefault(self.generator, []).append(tuple(row))
        elif name == "ORIGIN":
            self.is_origin = False

    def result(self):
        return self._result

    def convertSceneToScreenPosition(self, pos, matrix, width, height):
        rel_pos = np.squeeze(np.asarray(np.dot(matrix, pos)))
        rel_pos_unit = rel_pos / rel_pos[3]
        result = np.zeros(2)
        result[0] = (0.5 + 0.5 * rel_pos_unit[0]) * width
        result[1] = (0.5 - 0.5 * rel_pos_unit[1]) * height
        return result


def _write_data(data, path="./out.csv"):
    if os.path.exists(path) is True:
            print "file exists. skip"
            return
    np.savetxt(path, data,
               fmt=['%d'] * 2 + ['%.3f'] * 9, delimiter=" ",
               header=", ".join(MARKER_DT.names), comments='#')

def _arbaseline_remapping(data):
    #remove entries without ids
    idx = np.where(data['id'] == 0)
    data = np.delete(data, idx)
    # remap
    id_map = {47: 6, 42: 20, 137: 24, 20: 42, 6: 47, 24: 137}
    tmp = {}
    for k in id_map:
        tmp[k] = np.where(data['id']==k)
    for k, idx in tmp.items():
        data['id'][idx] = id_map[k]
    return data

def convert_data(path, trial, out='.'):
    #load tracker data

    con = ConfigLoader(trial)

    # hmd1.start should be roughly the time when the system was started
    time = con.get("hmd1.start")
    # study 1 lacks screen information
    matrix = HMD_MATRIX if trial < 200 else None  
    hmd = {}
    hmd = load_xcf_log(
        "%s/trial%d_hmd.xml" % (path, trial), time,
        matrix, 800, 600)
    cam = load_xcf_log(
        "%s/trial%d_cam3.xml" % (path, trial), time)
    if len(cam) != 1:
        raise Exception("something went wrong with cam3 tracker")

    # prepare and map data
    tracker = {}
    tracker['artkp_hmd1'] = hmd['lt3_artkp']
    tracker['artkp_hmd2'] = hmd['lt2_artkp']
    # filter table data
    data = filter_data(cam.values()[0], VELO_THRESHOLD)

    # normalize table data
    ext = RegionExtractor()
    points = ext.extract("%s/trial%d_cam3.mp4" % (out, trial))
    data['s_x'] -= points[0][0]
    data['s_x'] /= (points[1][0] - points[0][0])
    data['s_y'] -= points[0][1]
    data['s_y'] /= (points[1][1] - points[0][1])
    tracker['artkp_cam3'] = data
    if ('lt1_artkp' in hmd):
        tracker['artkp_top'] = hmd['lt1_artkp']

    #write data
    for generator in tracker:
        out_path = "%s/trial%d_%s.csv" % (out, trial, generator)
        if os.path.exists(out_path) is False:
            # during the first study another marker id mapping was used
            if trial/100 == 1:
                print "remap IDs"
                tracker[generator] = _arbaseline_remapping(tracker[generator])
            _write_data(tracker[generator], out_path)
        else:
            print "output file already exists. skipping."

def main(argv=None):
    if 'C5_RAW_PATH' not in os.environ:
        print "ERROR: ENV C5_RAW_PATH not set!"
        return 1
    if 'C5_VOL_PATH' not in os.environ:
        print "ERROR: C5_VOL_PATH not set!"
        return 1
    if argv is None:
        argv = sys.argv
    if argv[1] == 'convert':
        if 'all' in argv[2]:
            dic = TRIALS
        else:
            tid = int(argv[2])
            dic = {STUDIES[tid/100-1]:[tid]}
        for study, trials in dic.items():
            # skip 2nd trial since no markers were used
            if "NoAR" in study:
                continue
            for trial in trials:
                raw = "%s/%s/trial%d" % (RAW_PATH, study, trial)
                vol = "%s/%s/trial%d" % (VOL_PATH, study, trial)
                if check(raw, trial) is False:
                    print "data missing for trial %d. exit" % trial
                    return
                convert_data(raw, trial, vol)

if __name__ == "__main__":
    sys.exit(main())
