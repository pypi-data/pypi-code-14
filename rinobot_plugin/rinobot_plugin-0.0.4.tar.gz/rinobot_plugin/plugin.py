import os
import warnings
import argparse
import numpy as np


def loadfile(fpath, skiprows=0, **args):
    """
        loadfile(fpath, skiprows=0, **args)

        Loads a file with numpy.loadtxt and will recursively skips headers.

        Parameters
        ----------
        fpath : string
            Path to file to load
        skiprows : int
            Number of rows to skip
        **args
            Extra arguments for numpy.loadtxt

        Returns
        -------
        data : array or None
            Returns and array is possible
            and None if no data was found
    """
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        try:
            return np.loadtxt(fpath, skiprows=skiprows, **args)
        except ValueError:
            return np.loadtxt(fpath, skiprows+1)
        except StopIteration:
            return None


parser = argparse.ArgumentParser()
parser.add_argument('filepath', type=str)
parser.add_argument('--prefix', type=str)
parser.add_argument('--cols', type=str)
parser.add_argument('--rows', type=str)


def reset_parser():
    global parser
    parser = argparse.ArgumentParser()
    parser.add_argument('filepath', type=str)
    parser.add_argument('--prefix', type=str)
    parser.add_argument('--cols', type=str)
    parser.add_argument('--rows', type=str)


class Args(object):
    prefix=None
    filepath=None
    cols=None
    rows=None


def add_argument(*args, **kwargs):
    parser.add_argument(*args, **kwargs)


def get_args():
    args, unknown = parser.parse_known_args(namespace=Args())
    return args


def get_arg(arg, type=None, *args, **kwargs):
    if type:
        add_argument('--%s' % arg, type=type, *args, **kwargs)
    args, unknown = parser.parse_known_args(namespace=Args())
    return getattr(args, arg)


def is_plugin():
    args = get_args()
    if args.prefix:
        return True
    else:
        return False


def filepath():
    args = get_args()
    return args.filepath


def filename():
    args = get_args()
    return os.path.basename(args.filepath)


def no_extension():
    return os.path.splitext(filename())[0]


def output_filepath(fname):
    args = get_args()

    prefix = ''
    if args.prefix:
        prefix = args.prefix

    return os.path.join(
        os.path.dirname(filepath()),
        prefix + fname
    )


def to_int(a):
    try:
        return int(a)
    except ValueError:
        return None


def build_1d_index(s):
    if "::" in s:
        _i = tuple(map(to_int, s.split("::")))
        if len(_i) == 2:
            index = (_i[0], None, _i[1],)
        if len(_i) == 3:
            index = (_i[0], _i[2], _i[1],)

        _r = slice(*index)

    elif ":" in s:
        index = tuple(map(to_int, s.split(':')))
        _r = slice(*index)
    else:
        _r = (to_int(s), )

    return _r


def build_index(data, cols_string, rows_string):
    """
        translates the cols_string and rows_string
        to numpy indices to access the data
    """

    if not cols_string and not rows_string:
        return (slice(None), slice(None), )

    if len(data.shape) == 1:
        return build_1d_index(cols_string)

    elif rows_string and not cols_string:
        return (
            build_1d_index(rows_string),
            slice(None)
        ,)

    elif rows_string:
        return (
            build_1d_index(rows_string),
            build_1d_index(cols_string)
        ,)

    else:
        return (
            slice(None),
            build_1d_index(cols_string)
        ,)


def index_from_args(data):
    cols_string = get_args().cols
    rows_string = get_args().rows

    return build_index(data, cols_string, rows_string)
