# -*- coding: utf-8 -*-

from scikits.audiolab import Sndfile
import numpy as np
import logging


def get_sound(in_file, sampling_rate=441, cutoff=None, silence=None, out=None):
    """
    A function for sound detection. Can write filtered audio files, too.

    Parameters
    ----------
    in_file: string
        Path to the target sound file.
    sampling_rate: int, optional
        Sample rate for evaluation.
        A smaller rate improves speed and gets less detailed. 
    cutoff: float, optional
        Silence threshold in dB. Has to be negative! If None the function will 
        return the maximum aplitude value. 
    silence: int, optional
        Minimal silence duration in ms. Smaller gaps between sound 
        occurences will be removed.
    out: string, optional
        Path to filtered sound file. If this parameter is set, 
        the function will write a filtered sound file to the path.

    Returns
    -------
    sound: list
        a list containing whether sound was detected (1) or not (0) at time t
    vals: list
        a list containing energy values

    """
    logger = logging.getLogger("c5.audio.getSound")
    in_file = Sndfile(in_file,'r')        
    sample_count = int(in_file.samplerate/sampling_rate)
    if silence is not None:
        silence_ts = sampling_rate * silence/1000.0
    if out is not None:
        out_file = Sndfile(out,'w', in_file.format, in_file.channels, 
                           in_file.samplerate)
        mute = np.zeros(sample_count)
    nframes = in_file.nframes
    sound = []
    vals = []
    while nframes > 0:
        nsample = min([nframes, sample_count])
        data = in_file.read_frames(nsample)
        # $ E = \frac 1 N \sum_{i=1}^N s_i $
        val = np.max(data**2)
        val = np.log10(val) * 10
        logger.debug("")
        if cutoff is None:
            res = val
            if out is not None: out_file.write_frames(data)
        elif val < cutoff :
            res = 0
            if out is not None: out_file.write_frames(mute)
        else:
            res = 1
            if out is not None: out_file.write_frames(data)
        sound.append(res)
        vals.append(val)
        nframes -= nsample
    if silence is not None and cutoff is not None:    
        last_idx = 0
        for idx, i in enumerate(sound):
            if i == 1:
                if idx - last_idx < silence_ts:
                    sound[last_idx:idx] = [1]*(idx - last_idx)
                last_idx = idx
    in_file.close()
    return sound, vals