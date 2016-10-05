# -*- coding: utf-8 -*-

import csv
from config import VOL_PATH


class ConfigLoader():
    DIRECTORY = 1;    MERGED_VIDEO = 2
    CAM1_VIDEO = 3;    CAM1_START = 4;    CAM2_VIDEO = 5;    CAM2_START = 6
    CAM3_VIDEO = 7;    CAM3_START = 8;    HMD1_VIDEO = 9;    HMD1_START = 10 
    HMD2_VIDEO = 11;    HMD2_START = 12;    MIC = 13;         MIC_START = 14
    HMD_XCF = 15;     TOP_XCF = 16;     TOP_TIME = 17;    BRIX1_LOG = 18
    BRIX2_LOG = 19;    SYNC1_LOG = 20;    SYNC2_LOG = 21;    KINECT_BIN = 22
    KINECT_START = 23

    def __init__(self, filename):
        reader = csv.reader(open(filename), delimiter=',')
        self.__data = []
        for row in reader:
            self.__data.append(row)

    def data(self):
        return self.__data

    def get(self, trial_id, column):
        tid = (trial_id % 100) + (trial_id/200) * 10
        #print tid
        #print self.__data[tid][column]
        return self.__data[tid][column]

def main(argv):
    loader = ConfigLoader('test_data/trials.csv')
    print loader.get(101, ConfigLoader.MERGED_VIDEO)
    print loader.get(110, ConfigLoader.CAM2_VIDEO)
    print loader.get(201, ConfigLoader.DIRECTORY)
    print loader.get(212, ConfigLoader.KINECT_BIN)


class PhaseInfo():
    NEGOTIATION = 7
    CHECK = 8
    PRESENTATION = 9
    FREE = 11

    def __init__(self, filename):
        reader = csv.reader(open(filename), delimiter=',')
        self.__data = []
        for row in reader:
            if row[0].startswith('#'):
                continue
            self.__data.append(row)

    def data(self):
        return self.__data

    def get(self, trial_id, phase):
        for row in self.__data:
            if (int(row[0]) == trial_id) and (int(row[1]) == phase):
                    return (int(row[3]), int(row[4]))
        print "Could not find information."
        return (0, 0)


def elan2csv():
    import xml.etree.ElementTree as ET
    from c5.config import ConfigLoader

    mapping = {
        'P01':  1,
        'P02':  2,
        'P03':  3,
        'P04':  4,
        'P05':  5,
        'P06':  6,
        'P07':  7,
        'P08':  8,
        'P09':  9,
        'P10': 10,
        'P11': 11,
        'P12': 12,
        'P13': 13,
        'P14': 14,
    }

    config = ConfigLoader(VOL_PATH+'/trials.csv')
    trial_ids = range(101,111)
    trial_ids.extend(range(201,213))
    #trial_ids = [206,207,208,212]
    csv="#trial,id,desc,start,stop\n"
    
    for trial in trial_ids:
        eaf_file = VOL_PATH + config.get(trial, config.DIRECTORY) + "/Trial%02u_zE.eaf" % (trial%100)
        print eaf_file
        tree = ET.parse(eaf_file)
        root = tree.getroot()
        # read times
        # maybe parsing to int would be a nice thing
        times_xml = root.find('TIME_ORDER')
        times = {}
        for child in times_xml.iter('TIME_SLOT'):
            times[child.attrib['TIME_SLOT_ID']] = child.attrib['TIME_VALUE']

        # prepare csv output
        for tier_xml in root.findall('TIER'):
            if tier_xml.attrib['TIER_ID'] != 'Zeiteinteilung':
                continue
            #create csv
            for anno in tier_xml.iter('ANNOTATION'):
                meta = anno[0]
                text = meta[0].text.strip()
                if text in mapping:
                    csv += "%u,%u,%s,%s,%s\n" % (trial, mapping[text], text,
                                 times[meta.attrib['TIME_SLOT_REF1']],
                                 times[meta.attrib['TIME_SLOT_REF2']])
                else:
                    print "unknown key in trial with %d: " % (trial) + text
    f = open('ca_times.csv', 'w')
    f.write(csv)
    f.close()
