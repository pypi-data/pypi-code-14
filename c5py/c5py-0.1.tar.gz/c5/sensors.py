# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as pl
import tempfile
import os
import struct
from zipfile import ZipFile
import pandas as pd
import pickle

import c5.config
import logging 
logger = logging.getLogger('c5.sensors')


MARKER_PATH = "{0}/marker_data.pkl"

# dv camera angle unknown
# shouldnt be necessary since we can rerun with screen xcf output
# dv_matrix = np.matrix([[2.3787,0,0,0],
#                       [0,3.17159,0,0],
#                       [0,0,-1.00002,1.00136e-05],
#                       [0,0,-1,1]])
# hmd camera matrx angle 26

class KinectLoader:
    """
    A utility to handle timestamped PNGs like a video file.

    Attributes
    ----------
    timestamp : int
        The timestamp of the current image. If set, it will be adapted to the closest available timestamp.
    image : numpy.array
        The image at the chosen timestamp.

    Parameters
    ----------
    zip_file : str or int
        The path to the file to be loaded. If zip_file is an int, it is treated as a 
        trial number and the corresponding negotiation phase will be loaded. 

    Raises
    ------
    KeyError
        when a key error

    Examples
    --------
    To load negotiation files by passing trial numbers, the c5 configuration must point to the location
    of the corpus data.

    .. plot::
        :include-source:

        from c5.sensors import KinectLoader
        import matplotlib.pyplot as pl
        player = KinectLoader(101)
        image, timestamp = player.forward(600)
        _ = pl.imshow(image)

    """

    def __init__(self, zip_file):
        if isinstance(zip_file, int):
            zip_file = ("%s/%s/trial%d/trial%d_kinect_negotiation.zip" %
                       (c5.config.VOL_PATH, c5.config.STUDIES[(zip_file/100)-1],
                        zip_file, zip_file))
        self._zip = ZipFile(zip_file)
        files = self._zip.namelist()
        self.folder = files.pop(0)
        offset = len(self.folder)+7
        tmp = []
        for t in files:
            # get timestamp from filename
            ts = t[offset:-4]
            if len(ts) > 0:
                tmp.append(int(ts))
        self._ts = np.array(tmp)
        self._ts.sort()
        self._idx = 0

    @property
    def timestamp(self):
        return self._ts[self._idx]

    @timestamp.setter
    def timestamp(self, value):
        idx = (np.abs(self._ts-value)).argmin()
        self._idx = idx

    @property
    def image(self):
        with self._zip.open("%skinect_%d.png" % (self.folder, self.timestamp)) as f:
            res = pl.imread(f)
        return res, self.timestamp

    def next(self, skip=0):
        """
        Return the next image from the archive and set timestamp accordingly.

        Attributes
        ----------
        skip : int, optional
            Skip the amount of images.

        Returns
        -------
        image : numpy.array
            Kinect depth image encoded as numpy array.
        timestamp : int
            Timestamp of image. 
        """
        self.idx += skip + 1
        with self._zip.open("%skinect_%d.png" % (self.folder, self._ts[self.idx])) as f:
            res = pl.imread(f)
        return self.image

    def forward(self, seconds):
        """
        Skip forward an amount of seconds.

        Attributes
        ----------
        seconds : int
            Amount of seconds to be skipped.

        Returns
        -------
        image : numpy.array
            Kinect depth image encoded as numpy array.
        timestamp : int
            Timestamp of image. 
        """
        goal = self.timestamp + abs(seconds*1000)
        while self.timestamp < goal:
            self._idx += 1
        return self.image

    def rewind(self, seconds):
        """
        Rewind an amount of seconds.

        Attributes
        ----------
        seconds : int
            Amount of seconds to rewind.

        Returns
        -------
        image : numpy.array
            Kinect depth image encoded as numpy array.
        timestamp : int
            Timestamp of image. 
        """
        goal = self.timestamp - abs(seconds*1000)
        while self.timestamp > goal:
            self.idx -= 1
        return res, self.ts[self.idx]

def load_brix_log(filename):
    tmp_fd, tmp_path = tempfile.mkstemp()
    tmp_file = open(tmp_path, 'w')
    with open(filename, 'r') as f:
        for line in f:
            l = line.replace(':', ',')
            v_arr = l.split(',')
            if len(v_arr) == 7:
                tmp_file.write(l)
            elif len(v_arr) == 13:
                try:
                    tmp = []
                    #print v_arr
                    for i in range(6):
                        msb = int(v_arr[(i*2)+1])
                        lsb = int(v_arr[(i*2)+2])
                        #print "%i : %i" % (msb, lsb)
                        c = struct.pack("B", msb) + struct.pack("B", lsb)
                        tmp.append(struct.unpack(">h", c)[0])
                    #print tmp
                    tmp_file.write("%s,%d,%d,%d,%d,%d,%d\n" %
                                  (v_arr[0], tmp[0], tmp[1], tmp[2],
                                   tmp[3], tmp[4], tmp[5]))
                except ValueError:
                    logger.info("dropped line", v_arr)
            else:
                logger.info("dropped line", v_arr)
    tmp_file.close()
    result = np.loadtxt(tmp_path, skiprows=1, delimiter=',',
                        dtype=c5.config.BRIX_DT)
    os.remove(tmp_path)
    return result


def load_marker_data(path=None):
    path = path if path is not None else MARKER_PATH.format(c5.config.DATA_PATH)
    marker = {}
    if os.path.exists(path):
        with open(path,'r') as f:
            marker = pickle.load(f)
    else: 
        marker = _merge_marker_data()
        with open(path,'w') as f:
            pickle.dump(marker, f)
    return marker


def _merge_marker_data():
    res = {}
    for study in c5.config.STUDIES:
        if 'NoAR' in study:
            continue # no marker data available for Face-To-Face Condition
        for tid in c5.config.TRIALS[study]:
            print tid
            conf = c5.config.ConfigLoader(tid)
            p = {}
            for m in ['hmd1','hmd2','cam3']:
                print m
                tmp = np.loadtxt("{0}/{1}/trial{2}/trial{2}_artkp_{3}.csv".format(
                                  c5.config.VOL_PATH, study, tid, m),
                                  dtype=c5.config.MARKER_DT)
                start = conf.get('trial.phase.negotiation.start')
                stop = conf.get('trial.phase.negotiation.stop')
                x = None
                for mid in np.unique(tmp['id']):
                    if mid < 1:
                        continue
                    tmp_id = tmp[tmp['id'] == mid]
                    slots = c5.data.create_slots(start, stop,
                                                 c5.config.SAMPLING_INTERVAL, tmp_id)
                    slots = pd.DataFrame(slots)
                    slots.drop('id', axis=1, inplace=True)
                    slots = slots.add_suffix('_m%d' % mid)
                    slots.rename(columns={'timestamp_m%d'%mid:'timestamp'}, inplace=True)
                    x = pd.DataFrame(slots) if x is None else pd.merge(x, slots, on='timestamp')
                p[m] = x
            y = pd.merge(p['hmd1'], p['hmd2'], on='timestamp', how='outer',
                         suffixes=('_hmd1', '_hmd2'))
            res[tid] = pd.merge(y, p['cam3'], on='timestamp', how='outer', suffixes=('','_cam3'))
    return res    

