''' TimeSeries SparseArray

    Often, in our machine learning models, we have 3 dimensional matricies:
    num_features x num_time x num_data

    num_features and num_data are guaranteed to be uniform across samples but
    num_time may vary. Storing as a full Numpy Array is too large, a Scipy
    sparse array is restrictive, and list of lists is unusable.

    This class represents a way to handle 3-D indexing and operations while
    keeping the array internally 2-D

    fenceposts: our term for things that separate 2D in specific 3D chunks
'''

import cPickle
import numpy as np

def farray(obj, fenceposts):
    # like numpy, this array wraps around `obj`
    return FenceArray3D(obj, fenceposts)


def map_3d_to_2d(arr):
    n_dims, n_timesteps, n_seqs = arr.shape
    arr_DM = arr.swapaxes(0, 2).reshape((-1, n_dims)).T
    fenceposts_Np1 = np.arange(0, (n_seqs + 1) * n_timesteps, n_timesteps)
    return arr_DM, fenceposts_Np1


def map_3d_to_fencearray(arr):
    arr_DM, fp_Np1 = map_3d_to_2d(arr)
    return FenceArray3D(arr_DM, fp_Np1)


class FenceArray3D(object):
    def __init__(self, array_2d, fenceposts):
        ''' Args
            ----
            array_2d: Numpy Array or nested list
                      2 dimensional (but really 3D) array
            fenceposts : Numpy Array or list
                         1 D array that separates array_2d into
                         many 2D arrays that should be 3D

                         fenceposts[n] gives start index of sequence n
                         fenceposts[n+1] gives stop index of sequence n
        '''

        self.array_2d = array_2d
        self.fenceposts = fenceposts
        time_lengths = [fenceposts[f_pi+1]-fenceposts[f_pi] for f_pi in fenceposts[:-1]]
        self.shape = (array_2d.shape[0], time_lengths, len(fenceposts)-1)

    def _map(self, data_i):
        ''' given data index, return all times for it '''
        return xrange(self.fenceposts[data_i], self.fenceposts[data_i+1])

    def slice(self, index_tuples):
        ''' index_tuples (for FenceArray3D)
            ([1d indexes], [3d indexes])

            pass the features you want and which data you want and
            it will return to you all the time sequences in a 3D array.
            If it is not NumPy castable, then return list... but
            the point is to be NumPy castable so one should usually specify
            a single patient at a time.
        '''
        dim_idx, data_idx = index_tuples
        idx_sizes = list(len(x) for x in index_tuples if not isinstance(x, int))
        max_depth = max(np.ndim(np.array(x)) for x in index_tuples)

        # we can do the dim part right away
        array_2d = self.array_2d[dim_idx, :]

        if isinstance(data_idx, int):  # if data_idx is 1 single number
            mapped_i = self._map(data_idx)
            response = np.array(array_2d[..., mapped_i])
        else:  # if many numbers -- return another FenceArray3D object
            new_fenceposts = np.unique([[self.fenceposts[d_i], self.fenceposts[d_i+1]] for d_i in data_idx])
            num_indexes = 0
            for d_i in data_idx:
                num_indexes += (self.fenceposts[d_i+1]-self.fenceposts[d_i])

            new_array_2d = np.zeros((self.array_2d.shape[0], num_indexes))
            cur_index = 0
            for d_i in data_idx:
                fp_i, fp_ip1 = self.fenceposts[d_i], self.fenceposts[d_i+1]
                new_array_2d[:, cur_index:cur_index+fp_ip1-fp_i] = self.array_2d[:, fp_i:fp_ip1]
                cur_index += (fp_ip1-fp_i)

            response = FenceArray3D(new_array_2d, new_fenceposts)
        return response

    def apply(self, func, inplace=False, *args):
        array_2d = func(self.array_2d, *args)
        if inplace:
            self.array_2d = array_2d
        else:
            return array_2d

    @classmethod
    def save(cls, inst, path):
        with open(path, 'w') as fp:
            cPickle.dump(inst, fp)

    @classmethod
    def load(cls, path):
        with open(path) as fp:
            return cPickle.load(fp)
