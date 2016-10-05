# -*- coding: utf-8 -*-

import c5.config
from c5.config import VOL_PATH, TRIALS, SYNC_XML
import oldconfig
import xml.etree.ElementTree as ET
from xml.dom.minidom import parse
import os.path


def write_config(data):
    print data['conf_name']
    if os.path.exists("./%s.json" % (data['conf_name'])):
        print "file exists. skip"
    if ('stop' not in data or 'nego_start' not in data or
       'check_start' not in data or 'pres_start' not in data):
        print "error in set %s" % data['conf_name']
        print data.keys()
        return
    new = c5.config.ConfigLoader()
    #print data.keys()
    new.set("trial.start", data['start'])
    new.set("trial.stop", data['stop'])
    new.set("trial.phase.negotiation.start", data['nego_start'])
    new.set("trial.phase.negotiation.stop", data['nego_stop'])
    new.set("trial.phase.check.start", data['check_start'])
    new.set("trial.phase.check.stop", data['check_stop'])
    new.set("trial.phase.presentation.start", data['pres_start'])
    new.set("trial.phase.presentation.stop", data['pres_stop'])
    new.set("trial.phase.free.start", data['free_start'])
    new.set("trial.phase.free.stop", data['free_stop'])
    if (data['hmd1_start'] > 0):
        new.set("hmd1.start", data['hmd1_start'])
    if (data['hmd2_start'] > 0):
        new.set("hmd2.start", data['hmd2_start'])
    new.set("cam1.start", data['cam1_start'])
    new.set("cam2.start", data['cam2_start'])
    new.set("cam3.start", data['cam3_start'])
    if data['mic_start'] > 0:
        new.set("mic.start", data['mic_start'])
    new.save("./%s.json" % (data['conf_name']), True)


def read_phases(trial, study, data):
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
    eaf_file = "%s/%s/trial%d/Trial%02u_zE.eaf" % (VOL_PATH, study, trial, (trial % 100))
    if os.path.exists(eaf_file) is False:
        print "%s does not exist. skip" % eaf_file
        return data
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
                if mapping[text] == oldconfig.PhaseInfo.NEGOTIATION:
                    data['nego_start'] = data['start'] + int(times[meta.attrib['TIME_SLOT_REF1']])
                    data['nego_stop'] = data['start'] + int(times[meta.attrib['TIME_SLOT_REF2']])
                elif mapping[text] == oldconfig.PhaseInfo.CHECK:
                    data['check_start'] = data['start'] + int(times[meta.attrib['TIME_SLOT_REF1']])
                    data['check_stop'] = data['start'] + int(times[meta.attrib['TIME_SLOT_REF2']])
                elif mapping[text] == oldconfig.PhaseInfo.PRESENTATION:
                    data['pres_start'] = data['start'] + int(times[meta.attrib['TIME_SLOT_REF1']])
                    data['pres_stop'] = data['start'] + int(times[meta.attrib['TIME_SLOT_REF2']])
                elif mapping[text] == oldconfig.PhaseInfo.FREE:
                    data['free_start'] = data['start'] + int(times[meta.attrib['TIME_SLOT_REF1']])
                    data['free_stop'] = data['start'] + int(times[meta.attrib['TIME_SLOT_REF2']])
                    data['stop'] = data['free_stop']
            else:
                print "unknown key in trial with %d: " % (trial) + text                
    return data


def xml2json(url, trial):
    dom = parse(url)
    sets = dom.documentElement.getElementsByTagName("Set")
    s=sets[trial%100 - 1]
    data = {}
    name = s.getAttribute("name")
    nr = name[-2:]
    attr = {}
    attr['hint'] = int(s.getAttribute("hint"))
    hint = attr['hint']
    for c in s.getElementsByTagName("Container"):
        vid = c.getAttribute("name")
        attr[vid] = c.getAttribute("used_events").split(',')
    # 1000/fps = ms pro frame => 1000/25 = 40
    time_diff = (int(attr['schulter1'][1]) - int(attr['schulter1'][0]))
    #print time_diff
    if "hmd1" in attr:
        hmd1_fps = (int(attr['hmd1'][1]) - int(attr['hmd1'][0]))
        hmd1_fps /= time_diff * 0.04
        data['hmd1_fps'] = hmd1_fps
        data['hmd1_start'] = hint - int(int(attr['hmd1'][0])*1000/hmd1_fps)
    else:
        data['hmd1_start'] = 0
    if "hmd2" in attr:
        hmd2_fps = (int(attr['hmd2'][1]) - int(attr['hmd2'][0]))
        hmd2_fps /= time_diff * 0.04
        data['hmd2_fps'] = hmd2_fps
        data['hmd2_start'] = hint - int(int(attr['hmd2'][0])*1000/hmd2_fps)
    else:
        data['hmd2_start'] = 0
    data['cam1_start'] = hint - int(attr['schulter1'][0])*40
    data['cam2_start'] = hint - int(attr['schulter2'][0])*40
    if "top" in attr:
        data['cam3_start'] = hint - int(attr['top'][0])*40
    else:
        data['cam3_start'] = hint - int(attr['schulter3'][0])*40
    audio = s.getElementsByTagName("Audio")
    if len(audio) > 0:
        mic_start = s.getElementsByTagName("Audio")[0].getAttribute("sync")
        data['mic_start'] = hint - int(float(mic_start) * 1000)
    else:
        data['mic_start'] = 0
    data['start'] = min(data['cam1_start'], data['cam2_start'],
                        data['cam3_start'])
    if data['mic_start'] > 0:
        data['start'] = min(data['start'], data['mic_start'])

    trial = int("%d%s" % (trial/100, nr))
    data['conf_name'] = "trial%d" % trial
    return data


def csv2json():
    old = oldconfig.ConfigLoader(
        "%s/trials.csv" % VOL_PATH)
    old_ca = oldconfig.PhaseInfo(
        "%s/ca_times.csv" % VOL_PATH)

    for study, trials in TRIALS.items():
        for trial in trials:
            data = {}
            data['hmd1_start'] = int(old.get(trial, old.HMD1_START))
            data['hmd2_start'] = int(old.get(trial, old.HMD2_START))
            data['cam1_start'] = int(old.get(trial, old.CAM1_START))
            data['cam2_start'] = int(old.get(trial, old.CAM2_START))
            data['cam3_start'] = int(old.get(trial, old.CAM3_START))
            data['mic_start'] = int(old.get(trial, old.MIC_START))
    
            if data['hmd1_start'] > 0:
                data['start'] = min(data['hmd1_start'], data['hmd2_start'],
                                    data['cam1_start'], data['cam2_start'],
                                    data['cam3_start'])
            else:
                data['start'] = min(data['cam1_start'], data['cam2_start'],
                                    data['cam3_start'])
    
            data = read_phases(trial, old_ca, data)
            data['conf_name'] = "trial%d" % trial
            write_config(data)


def convert_csv():
    csv2json()


def convert_xml():
    for study, trials in TRIALS.items():
        xml_path = "%s/%s/%s" % (VOL_PATH, study, SYNC_XML[study])
        for trial in trials:
            data = xml2json(xml_path, trial)
            data = read_phases(trial, study, data)
            write_config(data)

convert_xml()