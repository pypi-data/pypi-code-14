"""
Simple smoothing functions (f:trajectory->trajectory)
"""

import numpy as np
from scipy.signal import get_window, medfilt

from statsmodels.nonparametric.smoothers_lowess import lowess


def copy_trajectory(traj):
    """
    Just a test.
    """
    return traj.copy()


class FilterByCol(object):
    """
    Filter by a pre-defined column using a pre-diefined filter function (f:column-val->bool)
    """
    def __init__(self, col, f, verbose=False):
        self._col = col
        self._f = f
        self._verb = verbose

    def filter(self, traj):
        t = traj.copy()
        mask = t[self._col].apply(self._f)
        to_drop = t.index.values[np.where(np.logical_not(mask))[0]]        
        t.drop(to_drop, axis=0, inplace=True)
        if self._verb:
            print "Filter (id={}): dropping {} rows.".format(t.id, len(to_drop))
        return t


class FilterSpacial(object):
    def __init__(self, kind='window', window=("gaussian", 1.0), width=7, dropna=True):
        self._kind = kind
        self._window = window
        self._width = width
        self._dropna = dropna 

    def filter(self, traj):
        t = traj.copy()

        if self._kind == "window":
            # FIR filter
            win = get_window(window=self._window, Nx=self._width)
            win = win / win.sum()
            for c in traj.geo_cols:
                t[c] = np.convolve(t[c], win, mode="same")
            # Get rid of edge effects
            w = int(self._width/2)
            n = len(t)
            to_drop = t.index.values[range(w) + range(n-w, n)]
            t.drop(to_drop, axis=0, inplace=True)

        elif self._kind == "RMF":
            # Repeated median filter with the scales stored in self._width
            for scale in self._width:
                for c in traj.geo_cols:
                    t[c] = medfilt(t[c], scale)

        elif self._kind == "LOWESS":
            for c in traj.geo_cols:
                t[c] = lowess(t[c], range(len(t)), frac=1.0*self._width/len(t),
                              is_sorted=True, return_sorted=False)

        elif self._kind == "Mahalanobis-LOWESS":
            # TODO: implement this...
            pass

        else:
            raise NotImplementedError("Never got around to implementing {} filter".format(self._kind))

        if self._dropna:
            t.dropna(axis=0, subset=t.geo_cols, inplace=True)

        return t


class Sparcify(object):
    """ Make a sparse representation of a trajectory
    """
    def __init__(self, r=50, f=None):
        self._r = r
        self._f = f

    def filter(self, traj):
        t = traj.copy()
        t["segment_sparcify_n"] = 0
        t["segment_sparcify_meta"] = 0

        itr = t.iterrows()
        ix0, first_row = itr.next()
        x0, y0 = first_row[list(t.geo_cols)]

        segment = [ix0]

        for ix, row in itr:
            x, y = row[list(t.geo_cols)]
            if (x0-x)**2 + (y0-y)**2 > self._r**2:
                # drop all but the first point in the list and reset
                t.ix[segment[0], "segment_sparcify_n"] = len(segment)
                if self._f is not None:
                    t.ix[segment[0], "segment_sparcify_meta"] = self._f(t.ix[segment])
                t.drop(segment[1:], axis=0, inplace=True)
                segment = []
                x0, y0 = x, y
            segment.append(ix)

        # deal with final segment
        t.ix[segment[0], "segment_sparcify_n"] = len(segment)
        if self._f is not None:
            t.ix[segment[0], "segment_sparcify_meta"] = self._f(t.ix[segment])
        t.drop(segment[1:], axis=0, inplace=True)

        return t


class ClusterDBSCANish(object):
    def __init__(self, r=50, min_density=.01):
        """
        :param r: float
        :param min_density: float
        """
        self._r = r
        self._md = min_density

    @staticmethod
    def finalize_circle(t, current_set, center):
        t.ix[current_set[0], list(t.geo_cols)] = center
        t.ix[current_set[0], "DBSCAN_n"] = len(current_set)
        t.ix[current_set[0], "DBSCAN_meta"] = {"n": len(current_set)}
        t.drop(current_set[1:], axis=0, inplace=True)

    def cluster(self, traj):
        """
        cluster a trajectory into segments with radius r or density at least md, if the radius os larger. This produces
          a sparse representation of the trajectory, and keeps clusters together.
        Algorithm:
            1.  One pass over the points
            1.1 Add current point to current set
            1.2 re-compute center and radius
            1.3 if no longer inside allowed parameters (density too low, and radius over minimum) then split
                and reset.
        :param traj: Trajectory
        :return: Trajectory
        """
        t = traj.copy()
        t["DBSCAN_n"] = 0
        t["DBSCAN_meta"] = 0

        iter = t.iterrows()
        ix0, row = iter.next()

        current_set = [ix0]
        r = 0
        center = t.ix[ix0, list(t.geo_cols)].values

        dist = lambda p0, p1: ((p0 - p1) ** 2).sum() ** .5

        for ix, row in iter:
            current_point = t.ix[ix, list(t.geo_cols)].values
            new_n = len(current_set) + 1
            new_center = (center*(new_n-1) + current_point) / new_n
            new_r = dist(new_center, current_point)
            new_density = new_n / (np.pi * new_r ** 2)

            if dist(center, current_point) > r:
                # New point is not in circle, expand circle to include it?
                if new_r > self._r and new_density < self._md:
                    # finalize old circle
                    self.finalize_circle(t, current_set, new_center)
                    # reset
                    current_set = []
                    r = 0
                    center = current_point
                else:
                    # everything is fine, keep going and adjust old circle
                    r = new_r
                    center = new_center
            else:
                pass

            current_set.append(ix)

        # process the final circle
        self.finalize_circle(t, current_set, center)

        return t
