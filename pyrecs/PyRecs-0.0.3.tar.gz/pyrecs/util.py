import numpy as np
from typing import Iterable, List, Tuple


def matrix_to_dataset(matrix):
    """
    Turns a matrix into a set of data points. A data point is a point `(x, z)` where `x` is a vector of the input
    features (in this case, a row index and a column index), and `z` is the observed output.

    Parameters
    ----------
    matrix : np.matrix
        The matrix to be converted

    Returns
    -------
    X : List
        `(r, c)` tuples
    y : List
        Observed outputs
    """
    X = []
    y = []
    for r, row in enumerate(matrix):
        for c, val in enumerate(row):
            if val is not None and np.isfinite(val):
                X.append((r, c))
                y.append(val)
    return X, y


def dataset_to_matrix(X, y, dtype=None, shape=None):
    """
    Parameters
    ----------
    X : Iterable
        The input features

    y : Iterable
        The observed outputs

    dtype : np.dtype
        The data-type of the resulting matrix

    shape : Tuple[int, int]
        The shape of the resulting matrix. Can be useful if a user or item is not represented in the input dataset.

    Returns
    -------
    matrix : np.matrix
    """
    X, y = list(X), list(y)

    if shape == None:
        shape = (max(r for r, _ in X) + 1,
                 max(c for _, c in X) + 1)

    matrix = np.ones(shape, dtype=dtype) * np.nan

    for loc, val in zip(X, y):
        if val != None and np.isfinite(val):
            matrix[loc[0]][loc[1]] = val

    return matrix
