"""
Analysis module
"""
from termcolor import colored

import analysis_helper as ah
import cdp
import den as dn
from srnaseq import SRNASeq

#TODO: combine functions - mnt3dm and den, CDP and CDP-split
def single_ref_profile(seq_file_list, ref_file, nt, smoothWinSize=50,
                       fileFig=False, fileName='plot.pdf', min_read_size=18,
                       max_read_size=32, min_read_no=1, onscreen=False, no_csv=False,
                       ylim=0, pub=False, split=False):
    """
    Align reads of a single length to a single reference
    :param seq_file_list: [path/to/seq/, path/to/seq2,...] (list(str))
    :param ref_file: path/to/reference (str)
    :param nt: read length to align (int)
    :param smoothWinSize: window size for soothing profile (int)
    :param fileFig: generate a PDF (bool)
    :param fileName: PDF filename (str)
    :param min_read_size: exclude reads with lengths < min_read_size (int)
    :param max_read_size: exclude reads with lengths > max_read_size (int)
    :param min_read_no: exclude reads with counts below min_read_no (int)
    :param onscreen: display plot (bool)
    :param no_csv:  generate a CSV of alignment data (bool)
    :param ylim: +/- y limits on plot
    :param pub: publication plot with no axes, legend (bool)
    :param split: split aligned read counts by number of times a read aligns
    """
    """
    Aligns reads from a single read file to a single reference sequence for
    a single sRNA size.
    """
    seq, seq_name = _profile_load_files_shared(max_read_size, min_read_no, min_read_size, seq_file_list)
    dn.srna_profile(seq, seq_name, ref_file, nt, smoothWinSize, fileFig,
                    fileName, onscreen, no_csv, ylim, pub, split)


def single_ref_profile_21_22_24(seq_file_list, ref_file, smoothWinSize=50,
                                fileFig=True, fileName='plot.pdf', min_read_size=18,
                                max_read_size=32, min_read_no=1, onscreen=True, no_csv=False,
                                y_lim=0, pub=False, split=False):
    """
    Align reads of 21, 22 annd 24 nt to a single reference
    :param seq_file_list: [path/to/seq/, path/to/seq2,...] (list(str))
    :param ref_file: path/to/reference (str)
    :param nt: read length to align (int)
    :param smoothWinSize: window size for soothing profile (int)
    :param fileFig: generate a PDF (bool)
    :param fileName: PDF filename (str)
    :param min_read_size: exclude reads with lengths < min_read_size (int)
    :param max_read_size: exclude reads with lengths > max_read_size (int)
    :param min_read_no: exclude reads with counts below min_read_no (int)
    :param onscreen: display plot (bool)
    :param no_csv:  generate a CSV of alignment data (bool)
    :param ylim: +/- y limits on plot
    :param pub: publication plot with no axes, legend (bool)
    :param split: split aligned read counts by number of times a read aligns
    """
    seq, seq_name = _profile_load_files_shared(max_read_size, min_read_no, min_read_size, seq_file_list)
    dn.srna_profile_21_22_24(seq, seq_name, ref_file, smoothWinSize,
                             fileFig, fileName, onscreen, no_csv, y_lim, pub, split)


def _profile_load_files_shared(max_read_size, min_read_no, min_read_size, seq_file_list):
    """
    Shared function for loading seq files
    :param max_read_size: exclude reads with lengths > max_read_size (int)
    :param min_read_no: exclude reads with counts below min_read_no (int)
    :param min_read_size: exclude reads with lengths < min_read_size (int)
    :param seq_file_list: [path/to/seq/, path/to/seq2,...] (list(str))
    """
    print(colored("-----------------LOADING SEQUENCES----------------", 'green'))
    seq = SRNASeq()
    if len(seq_file_list) == 1:
        seq.load_seq_file(seq_file_list[0], max_read_size, min_read_no,
                          min_read_size)
    else:
        seq.load_seq_file_arg_list(seq_file_list, max_read_size, min_read_no,
                                   min_read_size)
    seq_name = ah.single_file_output(seq_file_list[0])
    if len(seq_file_list) > 1:
        for i in range(len(seq_file_list)):
            if i == 0:
                pass
            else:
                seq_name += "_{0}".format(ah.single_file_output(seq_file_list[i]))
    return seq, seq_name


def CDP(seq_file_list_1, seq_file_list_2, ref_file, nt,
        fileFig=False, fileName='plot.pdf',
        min_read_size=18, max_read_size=32, min_read_no=1, onscreen=False,
        no_csv=False, pub=True, processes=4):
    """
    Align reads of a single length to multiple references, and calculate counts only
    :param seq_file_list_1: [path/to/seq/, path/to/seq2,...] (list(str))
    :param seq_file_list_2: [path/to/seq/, path/to/seq2,...] (list(str))
    :param ref_file: path/to/reference (str)
    :param nt: read length to align (int)
    :param fileFig: generate a PDF (bool)
    :param fileName: PDF filename (str)
    :param min_read_size: exclude reads with lengths < min_read_size (int)
    :param max_read_size: exclude reads with lengths > max_read_size (int)
    :param min_read_no: exclude reads with counts below min_read_no (int)
    :param onscreen: display plot (bool)
    :param no_csv:  generate a CSV of alignment data (bool)
    :param pub: publication plot with no axes, legend (bool)
    :param processes: no of processes to generate at a time i.e. threads (int)
    """

    seq_1, seq_2, seq_name_1, seq_name_2 = _cdp_load_files_shared(max_read_size, min_read_no, min_read_size,
                                                                  seq_file_list_1,
                                                                  seq_file_list_2)

    cdp.cdp_no_split_alignment(seq_1, seq_2, seq_name_1, seq_name_2, ref_file, nt, fileFig,
                               fileName, onscreen,
                               no_csv, pub, processes)


def CDP_split(seq_file_list_1, seq_file_list_2, ref_file, nt,
              fileFig=False, fileName='plot.pdf',
              min_read_size=18, max_read_size=32, min_read_no=1, onscreen=False,
              no_csv=False, pub=False, processes=4):
    """
    Align reads of a single length to multiple references, and calculate counts only
    :param seq_file_list_1: [path/to/seq/, path/to/seq2,...] (list(str))
    :param seq_file_list_2: [path/to/seq/, path/to/seq2,...] (list(str))
    :param ref_file: path/to/reference (str)
    :param nt: read length to align (int)
    :param fileFig: generate a PDF (bool)
    :param fileName: PDF filename (str)
    :param min_read_size: exclude reads with lengths < min_read_size (int)
    :param max_read_size: exclude reads with lengths > max_read_size (int)
    :param min_read_no: exclude reads with counts below min_read_no (int)
    :param onscreen: display plot (bool)
    :param no_csv:  generate a CSV of alignment data (bool)
    :param pub: publication plot with no axes, legend (bool)
    :param processes: no of processes to generate at a time i.e. threads (int)
    """
    seq_1, seq_2, seq_name_1, seq_name_2 = _cdp_load_files_shared(max_read_size, min_read_no, min_read_size,
                                                                  seq_file_list_1,
                                                                  seq_file_list_2)

    cdp.cdp_split_alignment(seq_1, seq_2, seq_name_1, seq_name_2, ref_file,
                            nt, fileFig, fileName, onscreen, no_csv, pub, processes)


def _cdp_load_files_shared(max_read_size, min_read_no, min_read_size, seq_file_list_1, seq_file_list_2):
    """

    :param max_read_size: exclude reads with lengths > max_read_size (int)
    :param min_read_no: exclude reads with counts below min_read_no (int):
    :param min_read_size: exclude reads with lengths < min_read_size (int):
    :param seq_file_list_1: [path/to/seq/, path/to/seq2,...] (list(str))
    :param seq_file_list_2: [path/to/seq/, path/to/seq2,...] (list(st_2:
    :return: seq1(sRNASeq), seq2 (sRNASeq), seq_name_1 (str), seq_name_2 (str)
    """
    print(colored("-----------------LOADING SEQUENCES----------------", 'green'))
    seq_1 = SRNASeq()
    if len(seq_file_list_1) == 1:
        seq_1.load_seq_file(seq_file_list_1[0], max_read_size, min_read_no,
                            min_read_size)
    else:
        seq_1.load_seq_file_arg_list(seq_file_list_1, max_read_size, min_read_no,
                                     min_read_size)
    seq_2 = SRNASeq()
    if len(seq_file_list_2) == 1:
        seq_2.load_seq_file(seq_file_list_2[0], max_read_size, min_read_no,
                            min_read_size)
    else:
        seq_2.load_seq_file_arg_list(seq_file_list_2, max_read_size, min_read_no,
                                     min_read_size)

    seq_name_1 = ah.single_file_output(seq_file_list_1[0])
    if len(seq_file_list_1) > 1:
        for i in range(len(seq_file_list_1)):
            if i == 0:
                pass
            else:
                seq_name_1 += "_{0}".format(ah.single_file_output(seq_file_list_1[i]))
    seq_name_2 = ah.single_file_output(seq_file_list_2[0])
    if len(seq_file_list_2) > 1:
        for i in range(len(seq_file_list_2)):
            if i == 0:
                pass
            else:
                seq_name_2 += "_{0}".format(ah.single_file_output(seq_file_list_2[i]))
    return seq_1, seq_2, seq_name_1, seq_name_2


def reads_aligned_per_seq(seq_file_list, ref_file, nt, split,
                          min_read_len=18, max_read_len=32, min_read_no=1, processes=4):
    """
    Get RPMR alignments for each sequence file in the list - no plot
    :param seq_file_list: [path/to/seq/, path/to/seq2,...] (list(str))
    :param ref_file: path/to/reference (str):
    :param nt: read length to align (int)
    :param split: spit reads or not (bool)
    :param min_read_size: exclude reads with lengths < min_read_size (int)
    :param max_read_size: exclude reads with lengths > max_read_size (int)
    :param min_read_no: exclude reads with counts below min_read_no (int)
    :param pub: publication plot with no axes, legend (bool)
    :param processes: no of processes to generate at a time i.e. threads (int)
    """
    """
    Calculates normalised reads aligned to multiple reference sequences for each seq file individually

    Outputs a csv only (no scatter plot)
    """
    print(colored("-----------------LOADING SEQUENCES----------------", 'green'))
    loaded_seq_list = []  # list of SRNASeq objects
    loaded_seq_name_list = []  # list of seq names in same order
    for seq_file in range(len(seq_file_list)):
        seq = SRNASeq()
        seq.load_seq_file(seq_file_list[seq_file],
                          max_read_len,
                          min_read_no,
                          min_read_len)
        loaded_seq_list.append(seq)
        seq_name = ah.single_file_output(seq_file_list[seq_file])
        loaded_seq_name_list.append(seq_name)

    if split:
        cdp.cdp_no_split_single(loaded_seq_list, loaded_seq_name_list,
                                ref_file,
                                nt, processes)
    else:
        cdp.cdp_split_single(loaded_seq_list, loaded_seq_name_list,
                             ref_file,
                             nt, processes)
