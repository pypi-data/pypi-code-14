

"""
Classes for managing in-memory trajectories.
"""

import numpy as np
import pandas as pd
from sqlalchemy import create_engine


class Trajectory(pd.DataFrame):
    """
    A single trajectory is a DF of points, attributes, and computed values.
    Also a linked-list with next_traj to allow a series of computations transforming from trajectory to trajectory (smoothing, etc.)
    """

    def pointwise_compute(self, func, name):
        """
        Compute a value for each point in the trajectory, and add it as a new column.
        :param func: Trajectory->column
        :param name: what should we call this new column?
        :return: self
        """
        self["comp_{}".format(name)] = func(self)
        return self

    def trajectory_compute(self, func, name):
        """
        Compute a new trajectory based on this one
        :param func: the function to apply to this trajectory
        :param name: the name of the resulting trajectory
        :return: tuple (name, trajectory) representing the resulting trajectory 
        """        
        self.next_traj = (name, func(self))
        return self.next_traj 

    def get_next(self, depth):
        """
        get next_traj (recursive)
        :param depth: how deep is the trajectory to return?
        :return: Trajectory
        """
        if depth == 0:
            return self
        else:
            return self.next_traj[1].get_next(depth-1)

    def get_attr(self, attr):
        return self["attr_{}".format(attr)]

    def get_comp(self, comp):
        return self["comp_{}".format(comp)]

    def copy(self):
        # TODO: a constructor for this...
        new_traj = Trajectory(super(Trajectory, self).copy())
        new_traj.id = self.id
        new_traj.geo_cols = self.geo_cols
        return new_traj

    def limit_first(self, k):
        to_drop = self.index.values[range(k, len(self))]
        self.drop(to_drop, axis=0, inplace=True)
        return self

    def combine(self, other, combine_f, name):
        # combine the data
        combine_col = combine_f(self, other)
        data1 = self.ix[other.index.values[np.where(combine_col == 0)[0]]]
        data2 = other.ix[other.index.values[np.where(combine_col == 1)[0]]]
        data = pd.concat([data1, data2])
        data.sort_index(inplace=True)
        # build new Trajectory
        t = Trajectory(data)
        t.id = self.id
        t.geo_cols = self.geo_cols
        self.next_traj = (name, t)
        return self.next_traj


class TrajectorySet(object):
    """
    Represent a set of Trajectory objects, with associated metadata
    """

    def __init__(self):
        self.__trajectories = dict()
        self.depth = 0

    def copy(self):
        """
        :return: Shallow copy
        """
        cp = TrajectorySet()
        cp.__trajectories = self.__trajectories.copy()
        return cp

    def filter(self, func):
        """
        Discard some of the trajectories
        :param func: function f:Trajectory->bool ; selects which Trajectory to keep
        :return: self
        """
        self.__trajectories = {key: val for key, val in self.__trajectories.iteritems()
                               if func(val)}
        return self

    def apply(self, func):
        """
        Replace trajectories by applying a function
        :param func: f: Trajectory->Trajectory
        :return: self
        """
        self.__trajectories = {key: func(val) for key, val in self.__trajectories.iteritems()}
        return self

    def load_frame(self, data, id_col="TAG", time_col="TIME", geo_cols=("X", "Y"),
                    attr_cols=("NBS", "VARX", "VARY", "COVXY"), sort_time=True):
        """
        :param data:
        :param id_col: this is the column that identifies a trajectory in the db (ex. animal_id)
        :param time_col: doesn't have to be DateTime
        :param geo_cols: the position information
        :param attr_cols: the attributes of localizations to keep in the Trajectory object
        :param sort_time: sort the rows of each trajectory by time? (Default: True)
        :return: self
        """

        # Keep only the columns requested, and give indicative names
        cols = [time_col] + list(geo_cols) + list(attr_cols)
        col_names = ["TIME"] + list(geo_cols) + ["attr_{}".format(attr) for attr in attr_cols]

        # Make Trajectory objects
        for id_ in data[id_col].unique():
            self.__trajectories[id_] = Trajectory(data.loc[data[id_col] == id_, cols])
            self.__trajectories[id_].id = id_
            self.__trajectories[id_].geo_cols = geo_cols
            self.__trajectories[id_].columns = col_names
            self.__trajectories[id_].set_index("TIME", inplace=True)

            if sort_time:
                self.__trajectories[id_].sort_index(inplace=True)

        return self

    def load_sqlite(self, path, id_col="TAG", time_col="TIME", geo_cols=("X", "Y"),
                    attr_cols=("NBS", "VARX", "VARY", "COVXY"), sort_time=True):
        # Sqlite connect
        conn = create_engine('sqlite:///{}'.format(path))
        data = pd.read_sql_table("LOCALIZATIONS", conn)

        # Use the regular DataFrame loader
        return self.load_frame(data, id_col, time_col, geo_cols, attr_cols, sort_time)

    def get(self, id_):
        return self.__trajectories[id_]

    def get_final(self, id_):
        """
        Get the last trajectory in the computtation chain
        :param id_: the id of the trajectory to retrieve
        :return: Trajectory
        """
        return self.get(id_).get_next(self.depth)

    def iter(self):
        for id_ in self.__trajectories:
            yield self.__trajectories[id_]

    def ids(self):
        return self.__trajectories.keys()

    def pointwise_compute(self, func, name):
        for t in self.iter():
            t.get_next(self.depth).pointwise_compute(func, name)
        return self

    def trajectory_compute(self, func, name, depth=None):
        depth = depth or self.depth
        self.depth += 1
        for t in self.iter():
            t.get_next(depth).trajectory_compute(func, name)
        return self

    def combine(self, other, depth, other_depth, combine_f, name):
        trajs = self.ids()
        for id_ in trajs:
           self.get(id_).get_next(depth).combine(other.get(id_).get_next(other_depth), combine_f, name)
        return self

    def __repr__(self):
        ans = {}
        for t in self.iter():
            id = t.id
            d = ["raw ({})".format(t.shape[0])]
            for i in range(self.depth):
                name, next = t.get_next(i).next_traj
                d.append("{} ({})".format(name, next.shape[0]))
            ans[id] = d
        return pd.DataFrame(ans).T.__repr__()


if __name__ == "__main__":
   pass