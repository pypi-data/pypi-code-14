from __future__ import division, absolute_import, print_function
# from brite_etl.decorators import frame_operation


# @frame_operation
def hash_cols(df, cols=None):
    """Hash columns with MD5

    Returns a dataframe containing 1 MD5 hash of the
    selected contents of the passed dataframe

    Parameters
    ----------
    df : DataFrame
        The dataframe to hash
    cols : list of str, optional
        Which columns to hash (the default is None, which hashes all columns)

    Returns
    -------
    DataFrame
        Dataframe with hashes for selected columns
    """
    import hashlib

    def _hash(x):
        return hashlib.md5(str(x)).hexdigest()

    if not cols:
        return df.apply(_hash, axis=0)
    else:
        return df[cols].apply(_hash, axis=0)
