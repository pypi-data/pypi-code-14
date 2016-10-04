def stn_terciles_to_txt(below, near, above, stn_ids, output_file, missing_val=None):
    """
    Writes station tercile data to a text file

    ### Parameters

    - below - *NumPy array* - array of below normal values
    - near - *NumPy array* - array of near normal values
    - above - *NumPy array* - array of above normal values
    - output_file - *string* - text file to write values to
    - missing_val - *float or None* - value to consider missing - if None then don't consider
      anything missing (write all data), otherwise just write the missing_val in all columns
    """
    # Open output file
    f = open(output_file, 'w')
    # Loop over all stations
    f.write('id      below    near   above\n'.format())
    for i in range(len(stn_ids)):
        # If below, near, and above are equal to the missing value
        # specified, do not format them (leave them as is)
        if missing_val is not None and all([x == missing_val for x in [below[i], near[i],
                                                                       above[i]]]):
            f.write('{:5s}   {:4s}     {:4s}    {:4s}\n'.format(
                stn_ids[i], str(missing_val), str(missing_val), str(missing_val)
                )
            )
        else:
            f.write('{:5s}   {:4.3f}   {:4.3f}   {:4.3f}\n'.format(stn_ids[i], below[i], near[i],
                                                                   above[i]))
    # Close output file
    f.close()
