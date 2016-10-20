"""
Alignment post-processing module 
"""

import numpy


def fill_in_zeros(fwd_rvs_align_list, ref_len, nt):
    """
    Generate alignment counts for every nucleotide in the reference
    :param fwd_rvs_align_list:  list of sorted forwards and reverse alignments
    :param ref_len: number of nucleotides in the reference sequence (int)
    :param nt: length of the aligned reads (int)
    :return: reference_x_axis ([0,0,...] (list(int)) - length of ref seq,
             fwd_alignment_y_axis [2,4,5.2,6,....] (list(float)) - sense strand alignment count (positive),
             fwd_rvs_align_list [-3,-4,-5.6,...] (list(float)) - antisense strand alignment count (negative)
    """
    sorted_fwd_alignment = fwd_rvs_align_list[0]
    sorted_rvs_alignment = fwd_rvs_align_list[1]

    fwd_alignment_y_axis = [0] * ref_len
    revs_alignment_y_axis = [0] * ref_len

    reference_x_axis = list(range(0, ref_len))
    #Note alignment position for graphing is in the centre of the read (and not the 5' end)
    for i in sorted_fwd_alignment:
        fwd_alignment_y_axis[i[0] + int(nt / 2)] = i[1]
    for i in sorted_rvs_alignment:
        revs_alignment_y_axis[i[0] - int(nt / 2)] = i[1]

    # #Coverage per nucleotide instead - maybe use?
    #     for i in sorted_fwd_alignment:
    #         for j in range(nt):
    #             fwd_alignment_y_axis[i[0]+j]+=i[1]
    #     for i in sorted_rvs_alignment:
    #         for j in range(nt):
    #             revs_alignment_y_axis[i[0]-j]+=i[1]

    return reference_x_axis, fwd_alignment_y_axis, revs_alignment_y_axis


def calc_alignments_by_strand(fwd_rvs_align_list):
    """
    :param fwd_rvs_align_list: list of sorted forwards and reverse alignments
    :return: Total RPMR aligned for fwd and rvs strands (float)
    """
    sorted_fwd_alignment = fwd_rvs_align_list[0]
    sorted_rvs_alignment = fwd_rvs_align_list[1]
    fwd_align_count = 0
    rvs_align_count = 0
    for i in sorted_fwd_alignment:
        fwd_align_count += i[1]
    for i in sorted_rvs_alignment:
        rvs_align_count -= i[1]
    return fwd_align_count, rvs_align_count


def smooth(x, window_len, window='hamming'):
    """
    Smoothing function from scipy cookbook
    :param x:
    :param window_len:
    :param window:
    :return:
    """

    if x.ndim != 1:
        raise ValueError("smooth only accepts 1 dimension arrays.")

    if x.size < window_len:
        raise ValueError("Input vector needs to be bigger than window size.")

    if window_len < 6:
        return x

    if not window in ['flat', 'hanning', 'hamming', 'bartlett', 'blackman']:
        raise ValueError("Window is one of 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'")

    s = numpy.r_[x[window_len - 1:0:-1], x, x[-1:-window_len:-1]]
    if window == 'flat':  # moving average
        w = numpy.ones(window_len, 'd')
    else:
        w = eval('numpy.' + window + '(window_len)')

    y = numpy.convolve(w / w.sum(), s, mode='valid')
    return y[int(window_len / 2 - 1):-int(window_len / 2)]


