''' Often time series data may be too long for machines to
    handle. We need a good way of sub-sampling a long time
    series sequence.

    My plan is to for each data sequence, find the locations
    of the positive examples. Pick some number of them. And then
    subsample randomly for the negative examples bewteen the
    positive ones as well.
'''

import numpy as np


def subsample_array(A, num, return_indexes=False):
    indexes = np.sort(np.random.choice(xrange(A.size), size=num))
    if return_indexes:
        return indexes
    return A[indexes]


class LocalTimeSeriesSampler(object):
    ''' LocalTimeSeriesSampler

        Takes every single positive example but keeps only a
        local subset of the negative examples.

        Example:

        y = 0 0 0 0 0 1 0 0 0 0 0 0 0 0 1 0 1 0 1 0 0 1 0 0 0 0 0 0 1 0 0 0 0 1
        t = 1 2 3 4 5 6 7 8 9 a b c d e f g h i j k l m n o p q r s t u v w x y z

        First sequence: t = 1 2 3 4 5 6
        Second sequence: t = a b c d e f g h i j k l m
        Third sequence: t = o p q r s t u v w x y

        Args:
        pre_range <- number of local examples to take before every + example
             this should be large (50-500)
        post_range <- number of local examples to take after every + example
             this should be small (0-50)
        pos_frac <- fraction of positive examples to take (default 1)
    '''

    def _init__(self):
        pass

    def subsample(self, X, y, pre_range=100,
                              post_range=0,
                              pos_frac=1,
                              sample_by_out_dim=0):
        ''' Args
            ----
            X : np array
               a (F x T x D) matrix where F is # features,
               T is # time-steps, D is # data points.
            y : np array
                is a (O x T x D) matrix where O is # outcomes
            pos_frac : double
            pre_range : integer
            post_range : integer

            Returns
            -------
            sub_X : np array
                    a (F x t x D) matrix where t is a subset of T
            sub_y : np array
                    a (O x t x D) matrix (binary)
        '''

        assert pos_frac >= 0 and pos_frac <= 1, \
            'fraction of positive examples must be between 0 and 1'
        assert pre_range >= 0, 'pre_range must be greater than 0'
        assert post_range >= 0, 'pre_range must be greater than 0'
        assert len(X.shape) == 3, '<X> must be 3 dimensional.'
        assert len(y.shape) == 3, '<y> must be 3 dimensional.'
        assert list(np.unique(y)) == [0, 1], '<y> must only contain 0 or 1.'

        num_features, num_time, num_data = X.shape
        num_outcomes, _, _ = y.shape

        sub_X, sub_y = [], []
        for data_i in range(num_data):
            cur_y = y[sample_by_out_dim, :, data_i]

            # find indexes of positive samples
            cur_y_where_pos = np.where(cur_y > 0)[0]
            if pos_frac < 1:
                cur_y_where_pos = np.random.choice(
                    cur_y_where_pos,
                    int(cur_y_where_pos.shape[0]*pos_frac))

            indexes_to_keep = []
            for i in range(len(cur_y_where_pos[:-1])):
                cur_idx = cur_y_where_pos[i]
                nex_idx = cur_y_where_pos[i+1]

                s_i = cur_idx-pre_range
                e_i = cur_idx+post_range
                if e_i >= nex_idx:
                    e_i = nex_idx - 1

                cur_slice = range(s_i, e_i+1)
                indexes_to_keep += cur_slice

            # do same for last index
            cur_idx = cur_y_where_pos[-1]
            s_i = cur_idx-pre_range
            e_i = num_time - 1
            cur_slice = range(s_i, e_i+1)
            indexes_to_keep += cur_slice
            indexes_to_keep = np.array(indexes_to_keep)
            indexes_to_keep = np.sort(np.unique(indexes_to_keep[indexes_to_keep > 0]))

        sub_X = X[:, indexes_to_keep, :]
        sub_y = y[:, indexes_to_keep, :]
        return sub_X, sub_y


class RandomTimeSeriesSampler(object):
    ''' RandomTimeSeriesSampler

        Subsamples a number of sequences in a slightly smarter
        manner than randomly. We assume that positive examples
        are sparser than negative examples.

        - positive examples are isolated and sampled randomly
        - negative examples are sampled in between each pair of
          positive examples.

        This way, the general structure should (hopefully) be
        preserved.
    '''

    def __init__(self):
        pass

    def subsample(self, X, y, perc):
        ''' Args
            ----
            X : np array
               a (F x T x D) matrix where F is # features,
               T is # time-steps, D is # data points.
            y : np array
                is a (O x T x D) matrix where O is # outcomes
            perc : double
                   % of pos and neg samples to keep

            Returns
            -------
            sub_X : np array
                    a (F x t x D) matrix where t is a subset of T
            sub_y : np array
                    a (O x t x D) matrix (binary)
        '''

        assert perc > 0, '<perc> must be greater than 0.'
        assert perc < 1, '<perc> must be less than 1.'

        assert len(X.shape) == 3, '<X> must be 3 dimensional.'
        assert len(y.shape) == 3, '<y> must be 3 dimensional.'
        assert list(np.unique(y)) == [0, 1], '<y> must only contain 0 or 1.'

        num_features, num_time, num_data = X.shape
        num_outcomes, _, _ = y.shape

        num_sample_time = int(num_time * perc)
        sub_X = np.zeros((num_features, num_sample_time, num_data))
        sub_y = np.zeros((num_outcomes, num_sample_time, num_data))

        for data_i in range(num_data):
            for out_i in range(num_outcomes):
                cur_y = y[out_i, :, data_i]

                # find indexes of positive samples
                cur_y_where_pos = np.where(cur_y > 0)[0]
                cur_y_where_neg = np.where(cur_y == 0)[0]

                # calc number in each sub sample
                sub_y_pos_num = int(cur_y_where_pos.size * perc)
                sub_y_neg_num = int((cur_y.size - cur_y_where_pos.size) * perc)

                # sub sample positive examples directly
                sub_y_where_pos = subsample_array(cur_y_where_pos, sub_y_pos_num)

                sub_y_where_neg = []
                sub_y_where_neg_pool = np.concatenate(([0], sub_y_where_pos, [cur_y.size]))

                # btwn each pair of + examples, sample a number of neg samples from there
                for pos_1, pos_2 in zip(sub_y_where_neg_pool[:-1], sub_y_where_neg_pool[1:]):
                    cur_y_neg_slice = cur_y_where_neg[np.logical_and(
                        cur_y_where_neg > pos_1, cur_y_where_neg < pos_2)]

                    if cur_y_neg_slice.size > 0:
                        sub_y_where_neg_slice = np.random.choice(
                            cur_y_neg_slice, int(cur_y_neg_slice.size*perc))
                        sub_y_where_neg.append(sub_y_where_neg_slice)
                sub_y_where_neg = np.concatenate(sub_y_where_neg)

                # find unsampled neg examples
                cur_y_where_neg_rem = np.setdiff1d(cur_y_where_neg, sub_y_where_neg)
                cur_y_where_neg_xtra = np.random.choice(
                    cur_y_where_neg_rem,
                    sub_y_neg_num - sub_y_where_neg.size + 1)
                sub_y_where_neg = np.append(sub_y_where_neg, cur_y_where_neg_xtra)

                # do the subsampling
                sub_where_keep = np.sort(np.concatenate((
                    sub_y_where_neg, sub_y_where_pos)))

                sub_X[:, :, data_i] = X[:, sub_where_keep, data_i]
                sub_y[:, :, data_i] = y[:, sub_where_keep, data_i]

        return sub_X, sub_y
