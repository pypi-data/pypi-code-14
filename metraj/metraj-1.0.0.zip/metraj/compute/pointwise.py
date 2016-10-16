"""
Pointwise computations
"""

import numpy as np


def position_det(trajectory, varx="VARX", vary="VARY", covxy="COVXY"):
    return trajectory.get_attr(varx)**.5 * trajectory.get_attr(vary)**.5 - trajectory.get_attr(covxy)


def position_max_var(trajectory,  varx="VARX", vary="VARY"):
    vx = trajectory.get_attr(varx)
    vy = trajectory.get_attr(vary)
    return map(np.max, zip(vx, vy))


def average_speed(trajectory, unix_time=True):
    """
    Compute the average speed between points in a trajectory (forward)
    :param trajectory: a Trajectory object
    :param unix_time: is the time format of the trajectory index unix time? Otherwise assume datetime
    :return: list of average speed between points
    """

    geo = trajectory[list(trajectory.geo_cols)].values
    t = trajectory.index.values

    dgeo = geo[1:, :] - geo[:-1, :]
    dt = t[1:] - t[:-1]
    return [0.0] + list((dgeo ** 2).sum(axis=1) ** .5 / dt * 1000)


def average_speed_sym(trajectory, unix_time=True):
    """
    Compute the symmetric min speed (forward and backward), defined as the minimum of the speed in each
    direction. This is used so that outliers are elliminated, but not the point after them.
    :param trajectory: a Trajectory object
    :param unix_time: is the time format of the trajectory index unix time? Otherwise assume datetime
    :return: list of min  (backwards or forwards) average speed between points.
    """
    geo = trajectory[list(trajectory.geo_cols)].values
    t = trajectory.index.values

    dgeo = geo[1:, :] - geo[:-1, :]
    dt = t[1:] - t[:-1]
    speed1 =  [0.0] + list((dgeo ** 2).sum(axis=1) ** .5 / dt * 1000)
    speed2 = list((dgeo ** 2).sum(axis=1) ** .5 / dt * 1000) + [0.0]

    return map(np.min, zip(speed1, speed2))


def first_passage_time(trajectory, r=50):
    """
    Compute the first passage time for each point
    :param trajectory:
    :param r:
    :return:
    """
    geo = trajectory[list(trajectory.geo_cols)].values
    ts = trajectory.index.values
    n = len(ts)

    fpt = np.zeros(n)

    t = 0   # the point we are computing FPT for

    sq_distance = lambda t0, t1: ((geo[t0] - geo[t1])**2).sum()

    for t in range(n):
        i = t
        while i < n - 1 and sq_distance(t, i) < r**2:
            i += 1
        fpt[t] = (ts[i] - ts[t]) / 1000  # convert to seconds

    return fpt



