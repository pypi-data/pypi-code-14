# -*- coding: utf-8 -*-

import os.path
from config_transform import xml2json
import subprocess


def check(path, trial):
    h1 = os.path.exists("%s/trial%d_hmd1.ogv" % (path, trial))
    h2 = os.path.exists("%s/trial%d_hmd2.ogv" % (path, trial))
    return (h1 and h2)


def fix_video(raw, vol, data, trial):
    for hmd in [1,2]:
        call = ['ffmpeg', '-i', "%s/trial%d_hmd%s.ogv" % (raw, trial, hmd),
                '-pix_fmt', 'yuv420p', '-r', str(25), "-preset", "slow", 
                "-crf", "18", '-filter:v',
                'setpts=%.8f*PTS' % (25.0/float(data['hmd%d_fps' % hmd])),
                "%s/trial%d_hmd%d.mp4" % (vol, trial, hmd)]
        print " ".join(call)
        subprocess.check_output(call)

def main():
    RAW_PATH = "/Volumes/FreeAgent GoFlex Drive/ARbC/raw"
    VOL_PATH = "/Users/alneuman/vol_c5/share/studies"

    t1 = range(101, 111)
    t3 = range(301, 306)
    t4 = range(401, 416)

    cor = {}
    cor['2011-12_ARBaseline'] = t1
    cor['2013-04_ExtAR'] = t3
    cor['2013-07_ARAssistance'] = t4

    xml = {}
    xml['2011-12_ARBaseline'] = "c5_AR.xml"
    xml['2013-04_ExtAR'] = "c5_ExtAR.xml"
    xml['2013-07_ARAssistance'] = "c5_ARAss.xml"

    for study, trials in cor.items():
        xml_path = "%s/%s/%s" % (VOL_PATH, study, xml[study])
        for trial in trials:
            raw = "%s/%s/trial%d" % (RAW_PATH, study, trial)
            vol = "%s/%s/trial%d" % (VOL_PATH, study, trial)
            if check(raw, trial):
                data = xml2json(xml_path, trial/100)
                fix_video(raw, vol, data, trial)
            else:
                print "check failed for trial %d" % trial

main()