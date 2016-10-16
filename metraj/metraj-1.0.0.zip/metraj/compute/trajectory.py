"""
a bunch of functions f:Trajectory->Trajectory
"""


class TrajectoryPart(object):
    @staticmethod
    def first(k):
        def first_k(traj):
            t = traj.copy()
            to_drop = t.index.values[range(k, len(traj))]
            t.drop(to_drop, axis=0, inplace=True)
            return t
        return first_k

    @staticmethod
    def keep_by_index(idx_list):
        def keep(traj):
            t = traj.copy()
            to_drop = [i for i in t.index.values if i not in idx_list]
            t.drop(to_drop, axis=0, inplace=True)
            return t
        return keep

