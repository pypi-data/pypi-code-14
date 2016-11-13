from functools import lru_cache

import numpy as np
import pandas as pd

from .util import dataset_to_matrix

_EPSILON = 0.00001

class CollaborativeFiltering(object):
    """Implements a memory-based collaborative filtering algorithm

    Algorithm based off of Breese, Heckerman, and Kadie, "Empirical Analysis of
    Predictive Algorithms for Collaborative Filtering"
    """
    def __init__(self):
        pass

    @lru_cache()
    def _weight(self, user_a, user_i):
        """Computes correlation between the given users"""
        a_votes = self._votes[user_a]
        i_votes = self._votes[user_i]

        a_mean = self._averages[user_a]
        i_mean = self._averages[user_i]

        item_ndx = np.logical_and(np.isfinite(a_votes),
                                  np.isfinite(i_votes))

        a_deviations = a_mean - a_votes[item_ndx]
        i_deviations = i_mean - i_votes[item_ndx]

        numerator = np.sum(a_deviations * i_deviations)
        denominator = (np.sum(np.power(a_deviations, 2)) *
                       np.sum(np.power(i_deviations, 2)))

        if denominator < _EPSILON:
            return 0
        return numerator / np.sqrt(denominator)

    def _predict_user_item(self, user, item):
        """Predicts the score of a given user for a given item"""
        if not isinstance(user, int):
            user = self._user_to_ndx[user]
        if not isinstance(item, int):
            item = self._item_to_ndx[item]

        try:
            rating_mean = self._averages[user]
        except AttributeError:
            raise RuntimeError('Must fit before predicting')

        other_users = [other for other in self._users if other != user and
                       np.isfinite(self._votes[other][item])]
        weights = np.array([self._weight(user, other)
                            for other in other_users])
        deviations = np.array([self._votes[other][item] - self._averages[other]
                               for other in other_users])

        weight_sum = np.sum(np.absolute(weights))
        if weight_sum < _EPSILON:
            return rating_mean  # No similar users, so guess their avg rating

        norm_const = 1 / weight_sum

        weighted_avg = np.sum(weights * deviations)
        return rating_mean + norm_const * weighted_avg

    def _fit_dataframe(self, df: pd.DataFrame, dtype):
        if len(df.index) != len(set(df.index)):
            raise ValueError('Non-unique values found in index')

        self._user_to_ndx = dict((u, n) for n, u in enumerate(df.index))
        self._item_to_ndx = dict((i, n) for n, i in enumerate(df.columns))

        self._votes = np.array(df.values, dtype=dtype)

    def fit(self, X, y=None, dtype=np.float64):
        if getattr(self, '_votes', None) is not None:
            raise RuntimeError('Already fit')

        if type(X) == pd.DataFrame:
            self._fit_dataframe(X, dtype=dtype)
        else:
            if y is None:
                raise RuntimeError('Must specify target (y)')

            self._votes = dataset_to_matrix(X, y, dtype=dtype)

        self._averages = np.zeros(self._votes.shape[0])
        self._users = range(self._votes.shape[0])

        for ndx, user_votes in enumerate(self._votes):
            self._averages[ndx] = np.mean(user_votes[np.isfinite(user_votes)])

    def predict(self, user_items):
        return np.array([self._predict_user_item(u, i) for u, i in user_items])
