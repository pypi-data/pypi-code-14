"""
Generate some trajectories
"""

import numpy as np
import pandas as pd

from metraj.trajectory import Trajectory


class TrajectoryGenerator(object):

    def __init__(self, drift=2, s=10, mr=200, d=1000, dilute=.25, startat=(0, 0)):
        """
        :param startat: tuple
            the starting point for the trajectory
        :param drift: float
            the rate of drift in static periods
        :param s: float
            measurement noise
        :param mr: float
            maximal radius of static point (std)
        :param d: float
            maximal length of locomotive period
        :param dilute: float (0, 1)
            percent of points to delete in the locomotive periods
        """
        self._p = list(startat)
        self._drift = drift
        self._s = s
        self._mr = mr
        self._d = d
        self._dilute = dilute

    def gen(self, nstatic, startat=None):
        # start the trajectory from this point
        if startat is not None:
            self._p = list(startat)

        points = []
        for i in range(nstatic):
            points.extend(self._get_locomotive())
            points.extend(self._gen_static())
        points.extend(self._get_locomotive())
        return self._points2traj(points)

    def _gen_static(self, n=1000):
        r = np.random.rand() * self._mr
        points = []
        last = np.array(self._p)
        for i in range(n):
            self._p[0] += self._drift * np.random.randn()
            self._p[1] += self._drift * np.random.randn()
            this_p = np.random.randn(2) * self._s + self._p + np.random.randn(2) * r
            this_p = .25*this_p + .75*last
            last = this_p
            points.append(list(this_p))
        return points

    def _get_locomotive(self, n=100):
        points = []
        dest = np.random.randn(2)*self._d + self._p
        points = zip(np.linspace(self._p[0], dest[0], n), np.linspace(self._p[1], dest[1], n))
        self._p = list(dest)

        # dilute
        ix = np.random.choice(len(points), int(len(points)*(1 - self._dilute)), replace=False)
        ix.sort()
        points = [points[i] for i in ix]

        return [list(np.random.randn(2) * self._s + p) for p in points]

    def _points2traj(self, points):
        t = Trajectory(points, columns=["X", "Y"])
        t.id = np.random.randint(1e6)
        t.geo_cols = t.columns
        return t
