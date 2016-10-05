""" Functions related to speech activity analysis. """

import subprocess
import numpy as np
import os.path
import pickle
import c5.config


SPEECH_DT = np.dtype({'names': ['timestamp', 'speech1', 'speech2'],
                     'formats': ['u8', 'i4', 'i4']})

SPEECH_PATH = "{0}/speech_activity.pkl"
ERODED_PATH = "{0}/speech_activity_eroded.pkl"
SPEECH_MAP = "{0}/speech_activity_map.png"

SOX_PARAMS = ['compand', '0.2,1', '-35,-19,-21,-7', '-1', '-35', '0.2']


def extract_speech_activity(wav_file, start, sampling_rate=50):
    """
    Load a wav sound file and resamples it into a numpy array with a constant sampling rate.

    Parameters
    ----------
    wav_file : str
        Path to a wav file
    start : int
        Timestamp of the recording's start.
    sampling_rate: int, optional
        Sampling rate of the returned array.

    Returns
    -------
    numpy.array or None
        Indexed array of the speech activity or None if wav_file does not exists or wav file is not processable.
    """
    from numpy.core.records import fromarrays
    import tempfile
    if os.path.exists(wav_file) is False:
        print "Warning: no %s found" % wav_file
        return None
    slots = None
    try:
        # split stereo channels
        left_fd, left_path = tempfile.mkstemp('.wav', prefix='left_')
        right_fd, right_path = tempfile.mkstemp('.wav', prefix='right_')

        # adapt volume
        subprocess.call(['sox', wav_file, left_path] + SOX_PARAMS + ['remix', '1'])
        subprocess.call(['sox', wav_file, right_path] + SOX_PARAMS + ['remix', '2'])

        # extract speech activity; ignoring energy values
        # default sampling rate of get_sound is 441 hz which is a decent trade off between accuracy and speed
        left_sound, _ = c5.audio.get_sound(left_path, cutoff=None)
        right_sound, _ = c5.audio.get_sound(right_path, cutoff=None)

        stop = int(start + len(left_sound) / 0.441)
        timestamps = np.arange(start=start, stop=stop, step=1 / 0.441)

        # in rare cases of rounding errors timestamps can be one element too long
        if timestamps.shape[0] - 1 == len(left_sound):
            timestamps = timestamps[:-1]
        data = np.column_stack((timestamps, left_sound, right_sound))
        data = fromarrays(data.transpose(), dtype=SPEECH_DT)
        slots = c5.data.create_slots(start, stop, 1000 / sampling_rate, data)
    except Exception as err:
        print "Error speech_activity: ", err
    finally:
        os.close(left_fd)
        os.close(right_fd)
        os.remove(left_path)
        os.remove(right_path)
    return slots


def load_speech_activity(path=None):
    """
    Load a previously preprocessed speech activity array or if it does not exist, generate an array from corpus data
    at C5_VOL_PATH and save it to C5_DATA_PATH.

    Parameters
    ----------
    path : str, optional
        Path to the pickled speech activity database. If not provided, C5_DATA_PATH will be checked instead.

    Returns
    -------
    dict(numpy.array)
        A dictionary with trial ids as keys and additional 'meta' information.
    """
    path = path if path is not None else SPEECH_PATH.format(c5.config.DATA_PATH)
    if os.path.exists(path):
        with open(path, "r") as f:
            db = pickle.load(f)
    else:
        db = _preprocess_data()
        db['meta'] = _get_meta(db.keys())
        with open(SPEECH_PATH, "w") as f:
            pickle.dump(db, f)
    return db


def load_eroded_speech(path=None, db=None, thresh=1000):
    """
    Load a previously eroded speech activity array or if it does not exist, erode the data in the passed db instead.

    Parameters
    ----------
    path : str, optional
        Path to the pickled eroded speech activity database. If not provided, C5_DATA_PATH will be checked instead.
    db : dict(numpy.array), optional
       A dictionary of speech activity arrays in the format returned by load_speech_activity.
    thresh : int
        Maximum duration in ms of signal gaps which will be removed by erosion.

    Returns
    -------
    dict(numpy.array)
        A dictionary of eroded speech activity with trial ids as keys and additional 'meta' information.

    Raises
    ------
    ValueError
        If neither path nor db were provided.
    """
    path = path if path is not None else ERODED_PATH.format(c5.config.DATA_PATH)
    if os.path.exists(path) and db is None:
        with open(path,'r') as f:
            ero = pickle.load(f)
    elif db is not None:
        ero = {}
        binary = _db_to_binary(db)
        for key in db:
            if key == 'meta': 
                ero[key] = db[key]
            else:
                # if thresh is None:
                ero[key] = _erode(binary[key], thresh)
                # else:
                #     tmp = binary[key]
                #     for idx, t in enumerate(thresh):
                #         tmp = _erode(tmp, thresh=t, signal=idx)
                #     ero[key] = tmp
        with open(path,'w') as f:
            pickle.dump(ero, f)
    else:
        raise ValueError('path does not exist and no speech data were provided')
    return ero


def _preprocess_data():
    db = {}
    for study in c5.config.STUDIES:
        for trial in c5.config.TRIALS[study]:
            trial_path = "%s/%s/trial%d" % (c5.config.VOL_PATH, study, trial)
            con = c5.config.ConfigLoader(trial, c5.config.VOL_PATH)
            wav_name = c5.config.FILE_NAMES['mic_wav'] % trial
            wav_file = "%s/%s" % (trial_path, wav_name)
            start = con.get("mic.start")
            slots = extract_speech_activity(wav_file, start)
            if slots:
                db[trial] = slots
            else:
                print "Error. No valid data for trial %d" % trial
    return db


def _db_to_binary(db):
    res = {}
    for key in db:
        res[key] = np.copy(db[key])
        if key == 'meta': continue
        # sil1 = min(-20, np.percentile(db[key]['speech1'], 60))
        # sil2 = min(-20, np.percentile(db[key]['speech2'], 60))
        # spe1 = min(-5, np.percentile(db[key]['speech1'][np.where(res[key]['speech1'] > sil1)], 75))
        # spe2 = min(-5, np.percentile(db[key]['speech2'][np.where(res[key]['speech2'] > sil2)], 75))
        res[key]['speech1'] = db[key]['speech1'] > -15
        res[key]['speech2'] = db[key]['speech2'] > -15
    return res


def _get_meta(keys, vol_path):
    meta = {}
    for key in keys:
        if key == 'meta':
            continue
        m = {}
        con = c5.config.ConfigLoader(key, vol_path)
        m['nego_start'] = con.get("trial.phase.negotiation.start")
        m['nego_stop'] = con.get("trial.phase.negotiation.stop")
        m['pres_start'] = con.get("trial.phase.presentation.start")
        m['pres_stop'] = con.get("trial.phase.presentation.stop")
        m['free_start'] = con.get("trial.phase.free.start")
        m['free_stop'] = con.get("trial.phase.free.stop")
        meta[key] = m
    return meta


def _erode(data, thresh, signal=1, columns=['speech1', 'speech2']):
    res = np.copy(data)
    res = np.sort(res, order='timestamp')
    for k in columns:
        last_idx = 0
        sound = res[k]
        for idx, i in enumerate(sound):
            if i == signal:
                if res[idx]['timestamp'] - res[last_idx]['timestamp'] <= thresh:
                    sound[last_idx:idx] = [signal]*(idx - last_idx)
                last_idx = idx
    return res