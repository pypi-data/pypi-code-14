import c5.config
import numpy as np
import os.path
import pickle

TURNTRANSITION_DT = np.dtype({'names': ['start', 'end', 'type', 'length_before', 'length', 'length_after'],
                              'formats': ['u8', 'u8', 'u8', 'u8', 'u8', 'u8']})
TURNS_PATH = "{0}/speech_activity_turns.pkl"


def load_turntaking(path=None, db=None):
    path = path if path is not None else TURNS_PATH.format(c5.config.DATA_PATH)
    seq = {}
    if os.path.exists(path) and db is None:
        with open(path,'r') as f:
            seq = pickle.load(f)
    elif db is not None:
        for trial, data in db.items():
            if isinstance(trial,int):
                seq[trial] = extract_turntaking(data)
        with open(path,'w') as f:
            pickle.dump(seq, f)
    else:
        raise ValueError('path does not exist and no speech data were provided')
    return seq


def extract_turntaking(data):
    tmp = np.zeros(data.shape[0], dtype=[('timestamp','u8'),('speech','i4')])
    tmp['timestamp'] = data['timestamp']
    tmp['speech'] = data['speech1'] + 2 * data['speech2']
    current = tmp[0]
    seq = []
    for x in tmp:
        if x['speech'] != current['speech']:
            seq.append((current['timestamp'], x['timestamp'], current['speech'],
                        0, x['timestamp']-current['timestamp'], 0))
            current = x
    x = tmp[-1]
    seq.append((current['timestamp'], x['timestamp'], current['speech'],
                0, x['timestamp']-current['timestamp'], 0))
    arr = np.array(seq, dtype = TURNTRANSITION_DT)
    return classify_turntaking(arr)


def classify_turntaking(seq):
    classed_seq = np.copy(seq)
    classed_seq[0]["length_after"] = classed_seq[1]["length"]
    for idx in range(len(seq)-2):
        classed_seq[idx+1]["length_before"] = seq[idx]["length"]
        classed_seq[idx+1]["type"] = str(seq[idx]["type"])+str(seq[idx+1]["type"])+str(seq[idx+2]["type"])
        classed_seq[idx+1]["length_after"] = seq[idx+2]["length"]
    classed_seq[-1]["length_before"] = seq[-2]["length"]
    return classed_seq


def turntaking_to_elan(switches, tid):
    switches = switches[np.where(switches['tid' == tid])]
    config = c5.config.ConfigLoader(tid)
    start_time = config.get('trial.start')
    switches['start'] -= int(start_time)
    dat = [[y['start'], int(y['start'] + y['duration']), 'Turnswitches', 1] for y in switches]
    np.savetxt("%s/trial%d_turns.csv" % (c5.config.DATA_PATH, tid), dat, delimiter=',', fmt='%s')


def filter_turntaking_types(seqf, types, length=2000):
    cons = []
    res = seqf
    for t in types:
        cons.append((res['type'] == t))
    res = res[np.where(np.logical_or.reduce(cons))]
    cons = ((res['length_before'] >= length), (res['length_after'] >= length))
    return res[np.where(np.logical_and.reduce(cons))]
