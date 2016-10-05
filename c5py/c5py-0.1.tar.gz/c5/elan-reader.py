
# coding: utf-8

# This is a converter of elan output-files to comma separated files

# In[1]:

import numpy as np
from csv import reader
from c5.config import VOL_PATH, STUDIES, TRIALS
import json
import os
from os import listdir
from os.path import isfile, join
import xml.etree.ElementTree as ET

IS_MAIN = __name__ == "__main__"


# Defining a dtype for annotation events:

# In[2]:

CA_FULL_DT = np.dtype({'names':['timestamp', 'tier', 'duration', 'content'], 
                    'formats':[np.uint64, np.object, np.uint, np.object]})

CA_VER_STRUK_DT = np.dtype({'names':['timestamp', 'person', 'duration', 'type', 'content'], 
                    'formats':[np.uint64, 'S1', np.uint, np.object, np.object]})
CA_VER_DEI_DT = np.dtype({'names':['timestamp', 'person', 'duration', 'type', 'content'], 
                    'formats':[np.uint64, 'S1', np.uint, np.object, np.object]})
CA_VER_PR_DT = np.dtype({'names':['timestamp', 'person', 'duration', 'referent', 'content'], 
                    'formats':[np.uint64, 'S1', np.uint, np.object, np.object]})
CA_VER_OR_DT = np.dtype({'names':['timestamp', 'person', 'duration', 'referent', 'content'], 
                    'formats':[np.uint64, 'S1', np.uint, np.object, np.object]})
CA_VER_DD_DT = np.dtype({'names':['timestamp', 'person', 'duration', 'content'], 
                    'formats':[np.uint64, 'S1', np.uint, np.object]})
CA_VER_LD_DT = np.dtype({'names':['timestamp', 'person', 'duration', 'content'], 
                    'formats':[np.uint64, 'S1', np.uint, np.object]})
CA_VER_TD_DT = np.dtype({'names':['timestamp', 'person', 'duration', 'content'], 
                    'formats':[np.uint64, 'S1', np.uint, np.object]})
CA_H_O_REL_DT = np.dtype({'names':['timestamp', 'person', 'side', 'duration', 'object', 'relation'], 
                    'formats':[np.uint64, 'S1', 'S1', np.uint, np.object, np.object]})
CA_DG_DT = np.dtype({'names':['timestamp', 'person', 'side', 'duration', 'referent'], 
                    'formats':[np.uint64, 'S1', 'S1', np.uint, np.object]})
CA_VER_DT = np.dtype({'names':['timestamp', 'person', 'duration', 'content'], 
                    'formats':[np.uint64, 'S1', np.uint, np.object]})
CA_ACTION_DT = np.dtype({'names':['timestamp', 'person', 'duration', 'content'], 
                    'formats':[np.uint64, 'S1', np.uint, np.object]})


# XML-Converter (Like ELAN-Export):

# In[3]:

def convert_eaf(eaf_file):
    if os.path.exists(eaf_file) is False:
        print("%s does not exist. skip" % eaf_file)
        return None
    tree = ET.parse(eaf_file)
    root = tree.getroot()
    
    times_xml = root.find('TIME_ORDER')

    times = {}

    for child in times_xml.iter('TIME_SLOT'):
        times[child.attrib['TIME_SLOT_ID']] = int(child.attrib['TIME_VALUE'])
    
    data=[]
    

    
    for tier_xml in root.findall('TIER'):
        tier_id = tier_xml.attrib['TIER_ID']
        for anno in tier_xml.iter('ANNOTATION'):
            meta = anno[0]
            time_start = times[meta.attrib['TIME_SLOT_REF1']]
            time_end = times[meta.attrib['TIME_SLOT_REF2']]
            duration = time_end - time_start
            text = meta[0].text
            data.append([tier_id, '', time_start, time_end, duration, text])
    return data


# Converter

# In[15]:

def convert_elan(elan_data, json_file):
    with open(json_file) as data_file:    
        json_data = json.load(data_file)
    start_time = np.min([json_data[device]['start'] for device in {'cam1', 'cam2', 'cam3', 'trial'}])

    new_data = []
    for x in elan_data:
        #Replacing ','s in the content to prepare for ',' delimiter. Not necessary, if elan-reader is gonna be used.
        if(x[5] == None):
            continue
        #content = np.core.defchararray.replace(x[5], ',', ';')
        event = (int(x[2])+start_time, str(x[0].encode('ascii','ignore')), int(x[4]), str(x[5].encode('ascii','ignore')))
        new_data.append(event)
    new_data = np.array(new_data, CA_FULL_DT)
    #sorting the data by timestamps (not sure if wanted)
    new_data = np.array(np.unique(new_data), dtype=CA_FULL_DT)
    return new_data


# ELAN-loader

# In[5]:

def load_annotations(folder_path):
    json = [f for f in listdir(folder_path) if isfile(join(folder_path, f)) and f.endswith(".json") and f.startswith("trial")]
    json_file = folder_path + json[0]
    final_files = [f for f in listdir(folder_path) if isfile(join(folder_path, f)) and f.endswith("_final.eaf")]
    if len(final_files) is 1:
        return convert_elan(convert_eaf(folder_path + final_files[0]), json_file)
    else:
        # Collecting data from several not final .eaf-files
        data =None
        for d in [ join(folder_path, f) for f in listdir(folder_path) if isfile(join(folder_path,f)) and f.endswith('.eaf') and not f == 'Trial05_final.eaf']:
            if data == None:
                data = convert_eaf(d)
            else:
                data = np.concatenate((data, convert_eaf(d)))
        data2 = data
        return convert_elan(np.array(data2), json_file)


# In[6]:

def get_study(trial):
    for study in STUDIES:
        if trial in TRIALS[study]: return study
    return False

def load_trial_annotation(trial):
    study = get_study(trial)
    assert(study)
    folder_path = "%s/%s/trial%d/" % (VOL_PATH, get_study(trial), trial)
    return load_annotations(folder_path)


# Verbal deixis specific extractors:

# In[16]:

def verbal_deixis(full_data):
    assert(full_data.dtype == CA_FULL_DT)
    partial_data = [(x[0], x[1][0], x[2], x[3].split(" ", 1)[0], x[3].split(" ", 1)[1]) for x in full_data if x[1].find("-ver-dei")==1]
    return np.array(partial_data, dtype = CA_VER_DEI_DT)

def verbal_object_reference(data):
    assert(data.dtype == CA_FULL_DT or data.dtype == CA_VER_DEI_DT)
    if(data.dtype == CA_FULL_DT):
        dat = verbal_deixis(data)
    else:
        dat = np.array(data, dtype=CA_VER_DEI_DT)
    partial_data = [(x[0], x[1], x[2], x[3].split("_")[-1], x[4]) for x in dat if x[3].find("or_")==0]
    return np.array(partial_data, dtype = CA_VER_OR_DT)

def verbal_personal_reference(data):
    assert(data.dtype == CA_FULL_DT or data.dtype == CA_VER_DEI_DT)
    if(data.dtype == CA_FULL_DT):
        dat = verbal_deixis(data)
    else:
        dat = np.array(data, dtype=CA_VER_DEI_DT)
    partial_data = [(x[0], x[1], x[2], x[3].split("_")[-1], x[4]) for x in dat if x[3].find("pr_")==0]
    return np.array(partial_data, dtype = CA_VER_PR_DT)

def verbal_discourse_deixis(data):
    assert(data.dtype == CA_FULL_DT or data.dtype == CA_VER_DEI_DT)
    if(data.dtype == CA_FULL_DT):
        dat = verbal_deixis(data)
    else:
        dat = np.array(data, dtype=CA_VER_DEI_DT)
    partial_data = [(x[0], x[1], x[2], x[4]) for x in dat if x[3].find("dd")==0]
    return np.array(partial_data, dtype = CA_VER_DD_DT)

def verbal_local_deixis(data):
    assert(data.dtype == CA_FULL_DT or data.dtype == CA_VER_DEI_DT)
    if(data.dtype == CA_FULL_DT):
        dat = verbal_deixis(data)
    else:
        dat = np.array(data, dtype=CA_VER_DEI_DT)
    partial_data = [(x[0], x[1], x[2], x[4]) for x in dat if x[3].find("ld")==0]
    return np.array(partial_data, dtype = CA_VER_LD_DT)

def verbal_temporal_deixis(data):
    assert(data.dtype == CA_FULL_DT or data.dtype == CA_VER_DEI_DT)
    if(data.dtype == CA_FULL_DT):
        dat = verbal_deixis(data)
    else:
        dat = np.array(data, dtype=CA_VER_DEI_DT)
    partial_data = [(x[0], x[1], x[2], x[4]) for x in dat if x[3].find("td")==0]
    return np.array(partial_data, dtype = CA_VER_TD_DT)


# Other specific extractors:

# In[8]:

def verbal_struk(full_data):
    assert(full_data.dtype == CA_FULL_DT)
    partial_data = [(x[0], x[1][0], x[2], x[3].split(" ", 1)[0], x[3].split(" ", 1)[1]) for x in full_data if x[1].find("-ver-struk")==1]
    return np.array(partial_data, dtype = CA_VER_STRUK_DT)

def hand_object_relation(full_data):
    assert(full_data.dtype == CA_FULL_DT)
    partial_data = []
    for x in full_data:
        if(x[1].find("H-O-rel") == 3):
            match = re.search('(\W+)(\w+[\+]?\w*)',x[3])
            partial_data.append((x[0], x[1][0], x[1][2], x[2], match.group(2), match.group(1)))
    return np.array(partial_data, dtype = CA_H_O_REL_DT)

def deictic_gesture(full_data):
    assert(full_data.dtype == CA_FULL_DT)
    partial_data = [(x[0], x[1][0], x[1][2], x[2], x[3][1:]) for x in full_data if x[1].find("dG")==3]
    return np.array(partial_data, dtype = CA_DG_DT)

def verbal_speech(full_data):
    assert(full_data.dtype == CA_FULL_DT)
    partial_data = [(x[0], x[1][0], x[2], x[3]) for x in full_data if x[1].find("_ver")==1]
    return np.array(partial_data, dtype = CA_VER_DT)

def action(full_data):
    assert(full_data.dtype == CA_FULL_DT)
    partial_data = [(x[0], x[1][0], x[2], x[3]) for x in full_data if x[1].find("-Handlung")==1]
    return np.array(partial_data, dtype = CA_ACTION_DT)


# #Examples

# In[19]:

if IS_MAIN:
    x = load_trial_annotation(105)
    print(np.unique(x['tier']))


# In[17]:

if IS_MAIN:
    lookup = {'H':24, 'BBQ':4, 'QP':47, 'WPA':137, 'NPA':64, 'FS':20, 'BS':6, 'BR':11, 'CP':19, 'HAB':1, 'KT':212, 'MG':42, 'NT':220, 'PZ':53, 'SP':50,
              'RC':70, 'WP':80, 'WS':171}
    for a in verbal_object_reference(x): 
        if a['referent'] not in lookup.keys(): print(a)


# In[18]:

if IS_MAIN:
    print(len([y for y in verbal_object_reference(x)['referent'] if y=="HAB"]))

