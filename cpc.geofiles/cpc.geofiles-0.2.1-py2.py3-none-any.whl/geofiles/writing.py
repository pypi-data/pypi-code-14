import numpy as np


def stn_terciles_to_txt(below, near, above, stn_ids, output_file, in_missing_val=None,
                        out_missing_val='nan'):
    """
    Writes station tercile data to a text file

    ### Parameters

    - below - *NumPy array* - array of below normal values
    - near - *NumPy array* - array of near normal values
    - above - *NumPy array* - array of above normal values
    - output_file - *string* - text file to write values to
    - in_missing_val - *float or None* - value to consider missing - if None then don't consider
      anything missing (except for None), otherwise just write the in_missing_val in all columns
    - output_missing_val - *string* - value to write to text file signifying missing data (defaults
    """
    # Open output file
    f = open(output_file, 'w')
    # Loop over all stations
    f.write('id      below    near   above\n'.format())
    for i in range(len(stn_ids)):
        # If below, near, and above are equal to the missing value
        # specified, do not format them (leave them as is)
        if np.isnan(in_missing_val):
            is_missing = all([np.isnan(x) for x in [below[i], near[i], above[i]]])
        elif in_missing_val is None:
            is_missing = all([x is None for x in [below[i], near[i], above[i]]])
        else:
            is_missing = all([x == in_missing_val for x in [below[i], near[i], above[i]]])
        if is_missing:
            f.write(
                '{:5s}   {:>5s}   {:>5s}   {:>5s}\n'.format(
                    stn_ids[i], out_missing_val, out_missing_val, out_missing_val
                )
            )
        else:
            f.write(
                '{:5s}   {:>4.3f}   {:>4.3f}   {:>4.3f}\n'.format(
                    stn_ids[i], below[i], near[i], above[i]
                )
            )
    # Close output file
    f.close()
