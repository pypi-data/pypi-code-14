# coding: utf-8

# In[86]:

import os
import os.path
import tempfile
import subprocess
import pickle

import numpy as np
import pylab as pl
from numpy.core.records import fromarrays

IS_MAIN = __name__ == "__main__"
if IS_MAIN:
    get_ipython().magic(u'matplotlib inline')
    from IPython.html import widgets # Widget definitions
    from IPython.display import display, Image # Used to display widgets in the notebook
    from IPython.html.widgets import interact, interactive, fixed
    pl.rcParams['figure.figsize'] = 16, 8

import c5.audio
import c5.config
import c5.data
import c5.output
from c5.config import VOL_PATH, TRIALS, FILE_NAMES, STUDIES, SAMPLING_RATE

SPEECH_DT = np.dtype({'names':['timestamp','speech1','speech2'],
                     'formats':['u8','i4','i4']})
SPEECH_PATH = "data/speech_activity.pkl"
ERODED_PATH = "data/speech_activity_eroded.pkl"
TURNS_PATH =  "data/speech_activity_turns.pkl"
SPEECH_MAP = "data/speech_activity_map.png"

SOX_PARAMS = ['compand', '0.2,1', '-35,-19,-21,-7', '-1', '-35','0.2']

if IS_MAIN:
    display(Image(filename='data/img/sfblogo.png'))


def amplify(ret_value):
    for line in ret_value.split('\n'):
        if 'RMS lev dB' in line:
            line = line.replace('RMS lev dB','')
            line = line.replace(' ', '')
            ret_value = float(line)
    if ret_value < -27.0:
        return ['gain','%.2f' % (-25 - ret_value)]
    else:
        return []


def db_to_binary(db):
    res = {}
    for key in db:
        res[key] = np.copy(db[key])
        if key == 'meta': continue
        sil1 = min(-20, np.percentile(db[key]['speech1'], 60))
        sil2 = min(-20, np.percentile(db[key]['speech2'], 60))
        spe1 = min(-5, np.percentile(db[key]['speech1'][np.where(res[key]['speech1'] > sil1)], 75))
        spe2 = min(-5, np.percentile(db[key]['speech2'][np.where(res[key]['speech2'] > sil2)], 75))
        res[key]['speech1'] = db[key]['speech1'] > spe1
        res[key]['speech2'] = db[key]['speech2'] > spe2
    return res


def get_meta(keys):
    meta = {}
    for key in keys:
        if key == 'meta': continue
        m = {}
        con = c5.config.ConfigLoader(key)
        m['nego_start'] = con.get("trial.phase.negotiation.start")
        m['nego_stop'] = con.get("trial.phase.negotiation.stop")
        m['pres_start'] = con.get("trial.phase.presentation.start")
        m['pres_stop'] = con.get("trial.phase.presentation.stop")
        m['free_start'] = con.get("trial.phase.free.start")
        m['free_stop'] = free_stop = con.get("trial.phase.free.stop")
        meta[key] = m
    return meta


def preprocess_data():
    db = {}
    for study, trials in TRIALS.items():
        for trial in trials:
            trial_path = "%s/%s/trial%d/" % (VOL_PATH, study, trial)
            con = c5.config.ConfigLoader(trial)
            wav_name = FILE_NAMES['mic_wav'] % trial
            wav_path = "%s/%s" % (trial_path, wav_name)
            if os.path.exists(wav_path) is False:
                print "Warning: no %s found" % wav_path
                continue
            try:
                # split stereo channels
                left_fd, left_path = tempfile.mkstemp('.wav',prefix='left_')
                right_fd, right_path = tempfile.mkstemp('.wav',prefix='right_')
                #ret_left = subprocess.check_output(['sox', wav_path, '-n', 'remix', '1', 'stats'], stderr=subprocess.STDOUT)
                #ret_right = subprocess.check_output(['sox', wav_path, '-n', 'remix', '2', 'stats'], stderr=subprocess.STDOUT)

                # adapt volume 
                subprocess.call(['sox', wav_path, left_path] + sox_compression + ['remix','1'])
                subprocess.call(['sox', wav_path, right_path] + sox_compression + ['remix', '2'])

            #     print subprocess.check_output(['sox', left_path, '-n', 'stats'], stderr=subprocess.STDOUT)
            #     print subprocess.check_output(['sox', right_path, '-n', 'stats'], stderr=subprocess.STDOUT)

                # extract speech activity; ignoring energy values
                left_sound, _ = c5.audio.get_sound(left_path, cutoff=None)
                right_sound, _ = c5.audio.get_sound(right_path, cutoff=None)

                start = con.get("mic.start")
                stop = int(start + len(left_sound)/0.441)
                timestamps = np.arange(start=0,stop=len(left_sound)/0.441, step=1/0.441)

                # in rare cases of rounding errors timestamps can be one element too long
                if (timestamps.shape[0]-1 == len(left_sound)):
                    timestamps = timestamps[:-1]
                timestamps += start
                data = np.column_stack((timestamps,left_sound,right_sound))
                data = fromarrays(data.transpose(), dtype=SPEECH_DT)
                slots = c5.data.create_slots(start,stop,1000/50,data)
                db[trial] = slots
            except Exception as err:
                print "Error trial %d: " % trial, err
            finally:
                os.close(left_fd)
                os.close(right_fd)
                os.remove(left_path)
                os.remove(right_path)
    return full


def load_speech_activity():
    if os.path.exists(SPEECH_PATH):
        with open(SPEECH_PATH, "r") as f:
            db = pickle.load(f)
    else:
        db = preprocess_data()
        db['meta'] = get_meta(full.keys())
        with open(SPEECH_PATH, "w") as f:
            pickle.dump(db, f)
    return db


if IS_MAIN:
    db = load_speech_activity()
    x = db_to_binary(db)
    y = np.copy(x[101])


# In[73]:

def erode(data, silence):
    res = np.copy(data)
    res = np.sort(res, order='timestamp')
    for k in ['speech1', 'speech2']:
        last_idx = 0
        sound = res[k]
        for idx, i in enumerate(sound):
            if i:
                t_cur = res[idx]['timestamp']
                t_last = res[last_idx]['timestamp']
                if res[idx]['timestamp'] - res[last_idx]['timestamp'] <= silence:
                    sound[last_idx:idx] = [1]*(idx - last_idx)
                last_idx = idx
    return res

def load_eroded_speech(db=None):
    ero = {}
    if os.path.exists(ERODED_PATH):
        with open(ERODED_PATH,'r') as f:
            ero = pickle.load(f)
    elif db is not None:
        ero = {}
        binary = db_to_binary(db)
        for key in db:
            if key == 'meta': 
                ero[key] = db[key]
            else:
                ero[key] = erode(binary[key], 1000)
        with open(ERODED_PATH,'w') as f:
            pickle.dump(ero, f)
    return ero

if IS_MAIN:
    ero = load_eroded_speech(db)
    print "* eroded data..."


# ### Speech Correlation

# In[23]:

def plot_speech_activity(db, ero, begin, end):
    b = begin
    e = max(begin+1,end)
    offset = db['timestamp'][0]
    db['timestamp'] -= offset
    pl.subplot(3,1,1)
    c5.output.format_time()
    pl.plot(db['timestamp'], db['speech1'])
    _ = pl.xlim(db['timestamp'][b], db['timestamp'][e])
    pl.subplot(3,1,2)
    c5.output.format_time()
    pl.plot(db['timestamp'],db['speech2'], 'g')
    _ = pl.xlim([db['timestamp'][b],db['timestamp'][e]])
    pl.subplot(3,1,3)
    pl.plot(ero['timestamp'],ero['speech1']+1.2)
    pl.plot(ero['timestamp'],ero['speech2'])
    overlap = np.logical_and(ero['speech1'], ero['speech2'])
    ts = ero['timestamp'][overlap > 0]
    pl.plot(ts, np.ones(ts.shape)+0.125, 'ro')
    _ = pl.xlim([ero['timestamp'][b], ero['timestamp'][e]])
    _ = pl.ylim((0,2.3))

def _plot_speech_activity(tid, begin, end):
    global db, ero
    tid = int(tid)
    plot_speech_activity(db[tid], ero[tid], begin, end)

if IS_MAIN:
    lst = [str(x) for x in sorted(db.keys())]
    x = interact(_plot_speech_activity, tid=lst,
                 begin=(0,49999), end=(1,50000))


# In[74]:

def calc_correlation(ero, sampling_rate):
    cor = {}
    data = np.copy(ero)
    data[:]['speech1'] = data[:]['speech1'] * 2 - 1
    data[:]['speech2'] = data[:]['speech2'] * 2 - 1
    data[:]['timestamp'] -= data[0]['timestamp']
    for size in [10,20,30]:
        cor[size] = c5.data.window_corr(data[:]['speech1'],
                                        data[:]['speech2'], 
                                        window=size*SAMPLING_RATE)
    return cor

if IS_MAIN:
    cors = {}
    for key in ero:
        if key == 'meta': continue
        cors[key] = calc_correlation(ero[key], 50)
    print "* correlation calculated ..."


# In[83]:

def plot_correlation(ero, meta, cor):
    ts = np.copy(ero['timestamp'])
    off = ts[0]
    ts -= off
    pl.hlines(0, 0, ts[-1],'r')
    pl.plot(ts, cor[10],'k', label="$\omega=$10s", lw=2)
    pl.plot(ts, cor[20],'c', label="$\omega=$20s", lw=3)
    pl.plot(ts, cor[30],'g', label="$\omega=$30s", lw=4)
    
    ph = [(meta['nego_start'] - off, meta['nego_stop'] - off),
          (meta['pres_start'] - off, meta['pres_stop'] - off),
          (meta['free_start'] - off, meta['free_stop'] - off)]
    for phase in ph:
        pl.axvspan(phase[0], phase[1], facecolor='k', alpha=0.2)
        
    pl.grid(True)
    c5.output.format_time()
    pl.xlim(ts[0], ts[-1])
    pl.ylim([-1.2,1.2])
    pl.legend(loc='lower right')
    #pl.gca().tick_params(axis='x', which='both', bottom='off', top='off', labelbottom='off')
    #pl.gca().tick_params(axis='y')
    

def _create_map():
    tmp_x, tmp_y = pl.rcParams['figure.figsize']
    pl.rcParams['figure.figsize'] = 30, 30
    dim = np.ceil(np.sqrt(len(ero)))
    idx = 1
    for k in range(101,516):
        if k not in ero:
            continue
        pl.subplot(dim,dim,idx)
        plot_correlation(cors[tid], ero[tid], ero['meta'][tid])
        pl.title('Trial %d' % k)
        idx += 1
    pl.savefig(SPEECH_MAP, bbox_inches='tight')
    pl.rcParams['figure.figsize'] = tmp_x, tmp_y
    pl.close()

def _plot_correlation(tid):
    global cors, ero
    tid = int(tid)
    pl.subplot(1,2,2)
    pl.gca().axis('off')
    pl.imshow(img)
    pl.subplot(1,2,1)
    plot_correlation(ero[tid], ero['meta'][tid], cors[tid])
    pl.title("Trial %d" % tid)

if IS_MAIN:
    if os.path.exists(SPEECH_MAP) is False:
        _create_map()
    img = pl.imread(SPEECH_MAP)
    lst = [str(x) for x in sorted(cors.keys())]
    x = interact(_plot_correlation, tid=lst)


# ### Turn Taking Overlap

# In[14]:

def plot_turn_overlap(ero, tid):
    data = ero[tid]
    con = c5.config.ConfigLoader(tid)
    nego_start = con.get("trial.phase.negotiation.start")
    nego_stop = con.get("trial.phase.negotiation.stop")
    data = data[data['timestamp'] > nego_start]
    data = data[data['timestamp'] < nego_stop]
    spoken = np.logical_or(data['speech1'], data['speech2']).sum() * 20
    overlap = np.logical_and(data['speech1'], data['speech2']).sum() * 20
    duration = float(nego_stop - nego_start)
    sample[tid/100].append(overlap/float(spoken))
    pl.plot(spoken/duration, overlap/float(spoken), colors[tid/100]+'o')
    pl.text(spoken/duration, overlap/float(spoken)+0.001, str(tid))

if IS_MAIN:
    sample = {1:[], 2:[], 3:[], 4:[], 5:[]}
    colors = ' brgck'
    for key in ero:
        if key == 'meta': continue
        i = key/100
        if i in range(1,6):
            plot_turn_overlap(ero, key)
        pl.xlabel('speech ratio')
        pl.ylabel('speech overlap')


# In[15]:

if IS_MAIN:
    from scipy import stats
    ps = np.ones((4,4))

    m = [1,2,4,5]

    for y in range(4):
        for x in range(4):
            ps[y,x] = stats.ks_2samp(sample[m[y]], sample[m[x]])[1]
    ax = pl.gca()
    ax.set_xticks(np.arange(ps.shape[1])+0.5, minor=False)
    ax.set_yticks(np.arange(ps.shape[0])+0.5, minor=False)
    # want a more natural, table-like display
    ax.invert_yaxis()
    ax.xaxis.tick_top()
    ax.set_xticklabels(sorted(m), minor=False)
    ax.set_yticklabels(sorted(m), minor=False)
    t = pl.pcolor(ps, alpha=0.8, edgecolor='k')
    t = pl.colorbar()

