import os
import json
import numpy as np
import pandas as pd
from fnmatch import fnmatch
from functools import reduce


def first(items):
    """
    Get the first item from an iterable.

    Warning: It consumes from a generator.

    :param items: an iterable
    :return: the first in the iterable
    """
    for item in items:
        return item


def jsonlines_reader(file_path, skip_decode_errors=False):
    """
    Yield each document in a JSON-lines document.
    :param file_path: filepath to a json-lines file set
    """
    with open(file_path) as fp:
        for line in fp:
            try:
                yield json.loads(line)
            except json.JSONDecodeError:
                if not skip_decode_errors:
                    raise


def files_processor(generator_func, dir_path, shell_ptn="*", recursive=False):
    for file_name in os.listdir(dir_path):
        file_path = os.path.join(dir_path, file_name)
        if recursive and os.path.isdir(file_path):
            for item in files_processor(generator_func, file_path,
                                        shell_ptn, True):
                yield item
        else:
            if fnmatch(file_name, shell_ptn):
                for item in generator_func(file_path):
                    yield item


def pd_print_entirely(frame_or_series):
    """
    Print a pandas dataframe or series in its entirety.

    :param frame_or_series: a pandas Series or DataFrame
    """
    columns = pd.get_option('display.max_columns')
    pd.set_option('display.max_columns', None)

    rows = pd.get_option('display.max_rows')
    pd.set_option('display.max_rows', None)

    try:
        print(frame_or_series)
    finally:
        pd.set_option('display.max_columns', columns)
        pd.set_option('display.max_rows', rows)


def np_and(condition, *conditions):
    # This is just much less noise then (a) && (b) && (c) to me.
    return reduce(np.logical_and, conditions, condition)


def np_or(condition, *conditions):
    # This is just much less noise then (a) || (b) || (c) to me.
    return reduce(np.logical_or, conditions, condition)

