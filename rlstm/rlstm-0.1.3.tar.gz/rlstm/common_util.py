import autograd.numpy as np


def safe_log(x, minval=1e-100):
    return np.log(np.clip(x, minval, 1))


def normalize(x, axis=1):
    row_sums = x.sum(axis=axis)
    return x / row_sums[:, np.newaxis]


def safe_pad(x, pad=1e-100):
    my_x = my_dstack([x, 1-x]) + pad
    my_shape = my_x.shape
    my_x = normalize(np.concatenate(my_x, axis=0), axis=1).reshape(my_shape)
    return my_x[:, :, 0]


def my_dstack(array_list):
    first = True
    for array in array_list:
        if len(array.shape) == 2:
            array = np.reshape(array, (array.shape[0], array.shape[1], 1))
        if first is True:
            out = array
            first = False
        else:
            out = np.concatenate((out, array), axis=2)
    return out


def merge_two_dicts(x, y):
    ''' Given two dicts, merge them into a new
        dict as a shallow copy. '''
    z = x.copy()
    z.update(y)
    return z


def format_preds(output_set1, output_set0):
    if np.ndim(output_set1) > 2:
        output_set1 = flatten_to_2d(output_set1, keep_dim=0).T
        output_set0 = flatten_to_2d(output_set0, keep_dim=0).T
    return np.dstack((output_set0, output_set1))


def format_preds(output_set1, output_set0):
    if np.ndim(output_set1) > 2:
        output_set1 = flatten_to_2d(output_set1, keep_dim=0).T
        output_set0 = flatten_to_2d(output_set0, keep_dim=0).T
    return np.dstack((output_set0, output_set1))


def flatten_to_2d(x, keep_dim=-1):
    return x.reshape((
        np.prod(x.shape) / x.shape[keep_dim],
        x.shape[keep_dim]))


def unique_rows(X):
    return np.unique(X.view(np.dtype((
        np.void, X.dtype.itemsize*X.shape[1])))).view(
        X.dtype).reshape(-1, X.shape[1])


def is_nominal(x):
    if isinstance(x, str) or isinstance(x, int):
        return True
    return False
