import re
import json
import tempfile
import cPickle
from datetime import datetime
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


def np_safe_to_int(A):
    return np.rint(A).astype(np.int64)


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


def wrapper_func(base_f, wrap_f):
    ' returns a function: g(f())'
    return lambda *args : wrap_f(base_f(*args))


def pp_json(json_thing, sort=True, indents=4):
    if type(json_thing) is str:
        print(json.dumps(json.loads(json_thing),
                         sort_keys=sort,
                         indent=indents))
    else:
        print(json.dumps(json_thing,
                         sort_keys=sort,
                         indent=indents))
    return None


def is_function(object):
    return hasattr(object, '__call__')


def is_json_serializable(object):
    try:
        json.dumps(object)
        return True
    except TypeError:
        return False


def is_pickle_serializable(object):
    try:
        with tempfile.TemporaryFile('w') as fp:
            cPickle.dump(object, fp)
            return True
    except TypeError:
        return False


def is_numpy_array(object):
    if type(object).__module__ in np.__name__:
        return True
    return False


def get_timestamp(safe=True):
    stamp = str(datetime.now())
    if safe:
        stamp = re.sub('\W+', '_', stamp)
    return stamp
