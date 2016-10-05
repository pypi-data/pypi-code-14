# -*- coding: utf-8 -*-

import numpy as np
import threading
import c5.config
from  matplotlib.mlab import rec_append_fields


def create_slots(start, stop, frame, data):
    if data.shape[0] == 0:
        tmp = []
        for i in range(len(data.dtype)):
            tmp.append(c5.config.DTYPE_DEFAULTS[data.dtype[i]])
        print tmp
        data = np.array([tuple(tmp)]*2, dtype=data.dtype)
        data[0]['timestamp']=stop+frame*2
    assert isinstance(data, np.ndarray), "data type is %s but numpy ndarray is required" % type(data)
    assert isinstance(data[0], np.void), "row type is %s but numpy void is required" % type(data[0])
    try:
        data[0]['timestamp']
    except ValueError:
        print "No timestamp field is set"
    data.sort(order='timestamp')
    result = []
    start -= start % frame
    stop += frame - stop % frame
    time = int(start)
    init_data = tuple([0]*len(data[0]))
    cur = np.array([init_data], dtype=data.dtype)[0]
    for it in data:
        while (it['timestamp'] > (time)) and (time <= stop):
            result.append(tuple([time]) + tuple(cur)[1:] + tuple([time-cur['timestamp']]))
            time += frame
        cur = it
    while time <= stop:
        result.append(tuple([time]) + tuple(cur)[1:] + tuple([time-cur['timestamp']]))
        time +=frame
    new_dt = np.dtype(data.dtype.descr + np.dtype([('delta',np.uint64)]).descr)
    return np.array(result,dtype=new_dt)


def sliding_window(data, func, window, stepsize=1):
    res = [0]*(window/stepsize)
    for idx in range(window, data.shape[0], stepsize):
        res.append(func(data[idx-window:idx]))
    return res


def weight_decay(x, last=0, b=0.95):
    c1 = (last + x) * b
    return c1


def window_corr(x, y, window, overlap=1):
    result = np.zeros(x.shape[0])
    window = int(window)
    for idx in range(window, x.shape[0]):
        a = x[idx-window:idx]
        b = y[idx-window:idx]
        result[idx] = np.sum(a*b)/float(window)
    return result


def window_sum(x,window, overlap=1):
    result = np.zeros(x.shape[0])
    window = int(window)
    for idx in range(window,x.shape[0]):
        result[idx] = x[idx-window:idx].sum()
    return result


def dict_to_array(db):
    dt = db[db.keys()[0]].dtype
    dt_col = ('tid', 'i4')
    dt_new = [dt_col]
    for field in dt.descr: dt_new.append(field)
    new = np.array([], dtype=dt_new)
    for tid, data in db.items():
        if not isinstance(tid, int):
            continue

        new_col = np.array(np.ones((data.shape[0])) * tid, dtype=[dt_col])
        new_rows = rec_append_fields(new_col, data.dtype.names, [data[n] for n in data.dtype.names])
        new = np.append(new, new_rows)
    return new


def frames_to_sequence(data, timestamps, dtype):
    stacked = np.vstack((timestamps, data)).transpose()
    last = stacked[0]
    res = []
    for s in stacked:
        if last[1] != s[1]:
            res.append((last[1], last[0], s[0], s[0]-last[0]))
            last = s
    s = stacked[-1]
    res.append((last[1], last[0], s[0], s[0]-last[0]))
    return np.array(res, dtype=[('data', dtype), ('start', 'u8'), ('end', 'u8'), ('duration', 'u8')])


def mollifier(size,e=1):
    result = []
    for x in np.arange(-e,e,2*e/float(size)):
        j = 1/e**2 * np.exp(-1/(1 - (x/e)**2))
        result.append(j)
    return np.array(result)


def norm_value_range(data):
    mn = np.min(data)
    mx = np.max(data)
    data -= mn
    if mx == mn: return
    data /= (mx-mn)


def resample(data, size):
    step = data.shape[0] / float(size)
    x = np.arange(start=0,stop=data.shape[0],step=step)
    xp = np.arange(data.shape[0])
    res = np.interp(x,xp,data)
    return res


def summarize(data, size):
    res = np.zeros(size)
    step = data.shape[0]/float(size)
    for idx,i in enumerate(np.arange(step,data.shape[0],step)):
        res[idx] = data[int(i-step):int(i)].sum()
    return res


def get_phase(data, trial=None, phase='negotiation', timestamps=None):
    tmp = {trial: data} if trial is not None else data

    for k, v in tmp.items():
        timestamps = v['timestamp'] if v.dtype.fields and "timestamp" in v.dtype.fields else timestamps

        if timestamps is None:
            raise ValueError('No timestamps provided!')

        if timestamps.shape[0] != v.shape[0]:
            raise ValueError('Dimension mismatch! Data dimension is %d but timestamps is %d' % 
                (v.shape[0], timestamps.shape[0]))

        con = c5.config.ConfigLoader(k, c5.config.VOL_PATH)
        phase_start = con.get("trial.phase.%s.start" % phase)
        phase_stop = con.get("trial.phase.%s.stop" % phase)

        filtered_before = timestamps > phase_start
        v = v[filtered_before]
        if timestamps.shape[0] != v.shape[0]:
            timestamps = timestamps[filtered_before]
        v = v[timestamps < phase_stop]
        tmp[k] = v
    return tmp[trial] if trial is not None else tmp


def unix_to_trial_time(data, key='trial.start'):
    ts = data['timestamp'][0]
    conf = c5.config.get_config(ts)
    data['timestamp'] - c5.config.get(key)


class WorkerThread(threading.Thread):
    def __init__(self, func, *args):
        threading.Thread.__init__(self)
        self.func = func
        self.args = args
        self.done = False

    def run(self):
        self.func(*self.args)
        self.done = True
        print "done"

    def is_done(self):
        return self.done