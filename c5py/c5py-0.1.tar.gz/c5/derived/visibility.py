import c5.config

import pandas as pd
import numpy as np
import os.path
import logging
import pickle

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

VISIBILITY_PATH = "%s/marker_visibility.pkl" % c5.config.DATA_PATH


def load_visibility_data(path=None, db=None):
    path = path if path is not None else VISIBILITY_PATH
    if os.path.exists(path) and db is None:
        with open(path, "r") as f:
            db = pickle.load(f)
    elif db is not None:
        visibility = {}
        for tid, data in db.items():
            logger.info('Processing trial %d', tid)
            visibility[tid] = get_visual_attention(data, 1000)
        with open(VISIBILITY_PATH, "w") as f:
            pickle.dump(db, f)
    else:
        raise ValueError("Either 'path' or 'db' has to be provided")
    return visibility


def get_visual_attention(data, thresh):
    data = data.copy()
    vis = {}
    for mid in c5.config.MARKER_IDS:
        cols = ["visible_m%d_hmd1" % mid, "visible_m%d_hmd2" % mid]
        tmp = pd.DataFrame(index=data.index, columns=cols)
        tmp = tmp.fillna(0)
        for hmd in ['hmd1', 'hmd2']:
            s_x = 's_x_m%d_%s' % (mid, hmd)
            s_y = 's_y_m%d_%s' % (mid, hmd)
            delta = 'delta_m%d_%s' % (mid, hmd)
            visible = 'visible_m%d_%s' % (mid, hmd)
            try:
                data.ix[(data[delta] > thresh), [s_x, s_y]] = np.nan
                x = (data[[s_x, s_y]] - 0.5).abs()
                tmp.ix[data[s_x] > 0, visible] = 0.5
                tmp.ix[(x[s_x] < 0.25) & (x[s_y]  < 0.25), visible] += 0.4
            except KeyError:
                logger.warn("No %d in for %s in trial" % (mid, hmd))
        vis[mid] = tmp
    cols = [data.timestamp]
    cols.extend(vis.values())
    return pd.concat(cols, axis=1)