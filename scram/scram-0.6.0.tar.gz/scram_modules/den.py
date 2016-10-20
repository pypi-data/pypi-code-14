from refseq import RefSeq
from termcolor import colored
from alignedreads import AlignedReads
import analysis_helper as ah
import numpy
import write_to_file as wtf
import post_process as pp
import plot_reads as pr
from multiprocessing import Process, JoinableQueue, Manager
import sys

"""
Module for generating sRNA alignment profiles
"""


def srna_profile(seq, seq_output, ref_file, nt, smooth_win_size, file_fig,
                 file_name, onscreen, no_csv, ylim, pub, split):
    """
    Align reads of one length to a single reference sequence
    :param seq: path/to/read file (str)
    :param seq_output: treatment name (str)
    :param ref_file: list of ref file paths (list(str))
    :param nt: read length to align (int)
    :param smooth_win_size: window size for smoothed profile (int)
    :param file_fig: output pdf (bool)
    :param file_name: manual file name (str)
    :param onscreen: display plot (bool)
    :param no_csv: generate CSV (bool)
    :param ylim: +/- y-limits for plot (int)
    :param pub: generate publication image (bool)
    :param split: split aligned read counts by number of times a read aligns (bool)
    """

    ref_output, single_ref = _load_ref_shared(ref_file)
    single_alignment = AlignedReads()
    single_alignment.align_reads_to_ref(seq, single_ref, nt)
    if split is False:
        single_alignment.split()
    single_sorted_alignments = single_alignment.aln_by_ref_pos(nt)
    if no_csv:
        wtf.csv_output(single_alignment,
                       nt,
                       seq_output,
                       ref_output)
    if file_fig or onscreen:

        graph_processed = pp.fill_in_zeros(single_sorted_alignments,
                                           len(single_ref), nt)
        x_ref = graph_processed[0]
        y_fwd_smoothed, y_rvs_smoothed = _smoothed_for_plot(graph_processed, smooth_win_size)

        if file_name == "auto":
            file_name = ah.ref_seq_nt_output(seq_output, ref_output, nt, "pdf")

        pr.den_plot(x_ref, y_fwd_smoothed, y_rvs_smoothed, nt, file_fig,
                    file_name, onscreen, ref_output, ylim, pub)


def srna_profile_21_22_24(seq, seq_output, ref_file, smooth_win_size,
                          file_fig, file_name, onscreen, no_csv, y_lim, pub, split):
    """
    Align reads of 21,22 and 24 nt to a single reference seq.
    :param seq: path/to/read file (str)
    :param seq_output: treatment name (str)
    :param ref_file: list of ref file paths (list(str))
    :param smooth_win_size: window size for smoothed profile (int)
    :param file_fig: output pdf (bool)
    :param file_name: manual file name (str)
    :param onscreen: display plot (bool)
    :param no_csv: generate CSV (bool)
    :param ylim: +/- y-limits for plot (int)
    :param pub: generate publication image (bool)
    :param split: split aligned read counts by number of times a read aligns (bool)
    """

    ref_output, single_ref = _load_ref_shared(ref_file)
    srna_lens = [21, 22, 24]
    work_queue = JoinableQueue()
    processes = []
    mgr = Manager()
    alignments_dict = mgr.dict()

    non_srt_alignments_dict = mgr.dict()  # for csv only
    for x in srna_lens:
        work_queue.put(x)
    for w in range(3):
        p = Process(target=_worker_21_22_24, args=(work_queue, seq, single_ref, split,
                                                   alignments_dict,
                                                   non_srt_alignments_dict,
                                                   no_csv))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()

    if file_fig or onscreen:

        graph_processed_21 = pp.fill_in_zeros(alignments_dict[21],
                                              len(single_ref), 21)
        graph_processed_22 = pp.fill_in_zeros(alignments_dict[22],
                                              len(single_ref), 22)
        graph_processed_24 = pp.fill_in_zeros(alignments_dict[24],
                                              len(single_ref), 24)

        x_ref = graph_processed_21[0]
        y_fwd_smoothed_21, y_rvs_smoothed_21 = _smoothed_for_plot(graph_processed_21, smooth_win_size)
        y_fwd_smoothed_22, y_rvs_smoothed_22 = _smoothed_for_plot(graph_processed_22, smooth_win_size)
        y_fwd_smoothed_24, y_rvs_smoothed_24 = _smoothed_for_plot(graph_processed_24, smooth_win_size)

        if file_name == "auto":
            file_name = ah.ref_seq_output(seq_output, ref_output, "pdf")

        pr.den_multi_plot_21_22_24(x_ref, y_fwd_smoothed_21, y_rvs_smoothed_21, y_fwd_smoothed_22, y_rvs_smoothed_22,
                                   y_fwd_smoothed_24, y_rvs_smoothed_24, file_fig, file_name, onscreen, ref_output,
                                   y_lim, pub)
    if no_csv:
        wtf.mnt_csv_output(non_srt_alignments_dict[21],
                           non_srt_alignments_dict[22],
                           non_srt_alignments_dict[24],
                           seq_output,
                           ref_output)


def _worker_21_22_24(work_queue, seq, single_ref, split, alignments_dict,
                     non_srt_alignments_dict,
                     no_csv):
    """
    Worker function for parallel processing - 21,22 and 24 alignments as separate processes
    :param work_queue:
    :param seq:
    :param single_ref:
    :param split:
    :param alignments_dict:
    :param non_srt_alignments_dict:
    :param no_csv:
    :return: True (required)
    """
    try:
        while not work_queue.empty():
            single_alignment = AlignedReads()
            srna_len = work_queue.get()
            single_alignment.align_reads_to_ref(seq, single_ref, srna_len)

            if split is False:
                single_alignment.split()
            if no_csv:
                non_srt_alignments_dict[srna_len] = single_alignment
            single_sorted_alignments = single_alignment.aln_by_ref_pos(srna_len)
            alignments_dict[srna_len] = single_sorted_alignments
    except Exception as e:
        print(e)
    return True


def _smoothed_for_plot(graph_processed, smooth_win_size):
    """
    Return fwd and rvs smoothed profiles
    :param graph_processed:
    :param smooth_win_size:
    :return:
    """
    y_fwd_smoothed = pp.smooth(numpy.array(graph_processed[1]),
                               smooth_win_size, window='blackman')
    y_rvs_smoothed = pp.smooth(numpy.array(graph_processed[2]),
                               smooth_win_size, window='blackman')
    return y_fwd_smoothed, y_rvs_smoothed


def _load_ref_shared(ref_file):
    """
    Shared function for loading reference file
    :param ref_file:
    :return:
    """
    ref = RefSeq()
    ref.load_ref_file(ref_file)
    single_ref = ""
    if len(ref) > 1:
        print("\nMultiple reference sequences in file. Exiting.\n")
        sys.exit()
    ref_output = ah.single_file_output(ref_file)
    for header in ref.headers():
        single_ref = ref[header]
    print(colored("------------------ALIGNING READS------------------\n", 'green'))
    return ref_output, single_ref
