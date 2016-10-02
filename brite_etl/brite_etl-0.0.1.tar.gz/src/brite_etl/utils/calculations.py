from __future__ import print_function
import sys, os

def sum_cols(df, cols):
    """Sum columns of Dataframe

    Parameters
    ----------
    df : DataFrame
        The dataframe to sum columns on
    cols : list of str
        The list of columns to sum. Should be numeric types

    Returns
    -------
    DataFrame
        A dataframe with summed columns
    """
    return df[cols].sum(axis=0)
