'''CDP analysis class - for calculation of reads aligning to a reference
sequence as (x,y) coordinates for two sets of sequence files

Created on 25 Feb 2016

@author: steve
'''
from termcolor import colored
from refseq import RefSeq
import write_to_file as wtf
import analysis_helper as ah
import plot_reads as pr
from dna import DNA
from multiprocessing import Process, JoinableQueue, Manager
import psutil
import time


def cdp_no_split_alignment(seq_1, seq_2, seq_name_1, seq_name_2, ref_file, nt, file_fig,
                           file_name, onscreen, no_csv, pub, cores):
    """
    Align two sets of sequence files to multiple reference sequences for scatter plotting of counts
    :param seq_1: seq file set 1 (SRNASeq)
    :param seq_2: seq file set 2 (SRNASeq)
    :param seq_name_1: seq set 1 name (str)
    :param seq_name_2: seq set 2 name (str)
    :param ref_file: pat/to/ref (str)
    :param nt: read length to align (int)
    :param file_fig: generate PDF (bool)
    :param file_name: PDF name (str)
    :param onscreen: show plot on screen (bool)
    :param no_csv: generate csv (boot)
    :param pub: publication images without labels, legend etc (bool)
    :param cores: number of processes to spawn (int)
    """
    start = time.time()
    workers = cores
    work_queue = JoinableQueue()
    processes = []
    mgr = Manager()
    count = 0
    counts_by_ref = mgr.dict()  # header:(count1, count2)
    refs = RefSeq()
    refs.load_ref_file(ref_file)
    print(colored("------------------ALIGNING READS------------------\n", 'green'))
    for header, seq in refs:
        work_queue.put((header, seq,))  # tuple into work queue
        count += 1
        if count % 10000 == 0:
            print ("{0} reference sequences processed\n".format(count))
            print (colored("{0}% system RAM used\n".format(psutil.virtual_memory().percent),'green'))
            _cdp_no_split_queue(counts_by_ref, nt, processes, seq_1, seq_2, work_queue, workers)
    _cdp_no_split_queue(counts_by_ref, nt, processes, seq_1, seq_2, work_queue, workers)
    print("\nAlignment time = " + str("{0:.1f}".format((time.time() - start))) + " seconds\n")
    if len(counts_by_ref) == 0:
        print("\nNo reads aligned to any reference sequence. \
        Output files not generated\n")
    else:
        _cdp_output(counts_by_ref.copy(), file_fig, file_name, onscreen, no_csv, seq_name_1,
                    seq_name_2, ref_file, nt, pub)


def _cdp_no_split_queue(counts_by_ref, nt, processes, seq_1, seq_2, work_queue, workers):
    """
    Fill the multiprocess queue for non-split CDP
    :param counts_by_ref: Manager dict for counts for each reference result (mgr.dict)
    :param nt: read length to align (int)
    :param processes: list for processes to be added to (list)
    :param seq_1: seq file set 1 (SRNASeq)
    :param seq_2: seq file set 2 (SRNASeq)
    :param work_queue: joinable queue with ref header and seq tuples (JoinableQueue(header,ref_seq))
    :param workers: number of processes to spawn (int)
    """
    for w in range(workers):
        p = Process(target=_cdp_no_split_worker, args=(work_queue, counts_by_ref,
                                                       seq_1,
                                                       seq_2,
                                                       nt))
        p.start()
        processes.append(p)
    for p in processes:
        p.join()


def _cdp_no_split_worker(work_queue, counts_by_ref, seq_1, seq_2, nt):
    """
    Worker process - get ref from work queue, aligns reads from seq_1 and seq_2,
    and adds as (x,y) coords to counts_by_ref if there are alignments.
    :param work_queue: joinable queue with ref header and seq tuples (JoinableQueue(header,ref_seq))
    :param counts_by_ref: Manager dict for counts for each reference result (mgr.dict)
    :param seq_1: seq file set 1 (SRNASeq)
    :param seq_2: seq file set 2 (SRNASeq)
    :param nt: read length to align (int)
    :return: True
    """

    try:
        while not work_queue.empty():
            both_aligned = _cdp_no_split_single_ref_align(work_queue.get(), seq_1, seq_2, nt)
            if both_aligned is not None:
                counts_by_ref[both_aligned[0]] = (both_aligned[1], both_aligned[2])
    except Exception as e:
        print(e)
    return True


def _cdp_no_split_single_ref_align(single_ref, seq_1, seq_2, nt):
    """
    Count for both seqs aligned to single ref seq
    :param single_ref: single ref seq (DNA)
    :param seq_1: seq file set 1 (SRNASeq)
    :param seq_2: seq file set 2 (SRNASeq)
    :param nt: read length to align (int)
    :return header, count_1, count 2 (str, float, float)
    """
    single_alignment = _cdp_no_split_count_aligned_reads_to_seq(seq_1, seq_2,
                                                                single_ref[1], nt)

    if single_alignment[0] != 0 or single_alignment[1] != 0:
        return single_ref[0], single_alignment[0], single_alignment[1],


def _cdp_no_split_count_aligned_reads_to_seq(seq_dict_1, seq_dict_2, ref, sRNA_length):
    """

    :param seq_dict_1:
    :param seq_dict_2:
    :param ref:
    :param sRNA_length:
    :return:
    """
    """
    For non-split alignments!

    Return mapped reads for a single ref_seq
    pos is 5' end of read relative to 5' end of fwd strand

    returns an integer
        :return: (aligned_count_1,aligned_count_2) (tuple(float,float))
    """

    aligned_count_1 = 0  # number of reads aligned
    aligned_count_2 = 0  # number of reads aligned
    count_start = 0

    ref_complement = ref.complement()

    while count_start < (len(ref) - (sRNA_length - 1)):
        query_seq_fwd, query_seq_rvs = _get_query_seqs(count_start, ref, ref_complement, sRNA_length)

        aligned_count_1 = _cdp_no_split_aligned_count(aligned_count_1, query_seq_fwd, query_seq_rvs, seq_dict_1)
        aligned_count_2 = _cdp_no_split_aligned_count(aligned_count_2, query_seq_fwd, query_seq_rvs, seq_dict_2)
        count_start += 1

    return (aligned_count_1,aligned_count_2)


def _get_query_seqs(count_start, ref, ref_complement, sRNA_length):
    """

    :param count_start:
    :param ref:
    :param ref_complement:
    :param sRNA_length:
    :return:
    """
    query_seq_fwd = DNA(ref[count_start:(count_start + sRNA_length)])
    query_seq_rvs = DNA(ref_complement[count_start:(count_start + sRNA_length)])
    return query_seq_fwd, query_seq_rvs


def _cdp_no_split_aligned_count(aligned_count_1, query_seq_fwd, query_seq_rvs, seq_dict_1):
    """

    :param aligned_count_1:
    :param query_seq_fwd:
    :param query_seq_rvs:
    :param seq_dict_1:
    :return:
    """
    if query_seq_fwd in seq_dict_1:
        aligned_count_1 += seq_dict_1[query_seq_fwd]
    if query_seq_rvs in seq_dict_1:
        aligned_count_1 += seq_dict_1[query_seq_rvs]
    return aligned_count_1


def cdp_split_alignment(seq_1, seq_2, seq_name_1, seq_name_2, ref_file,
                        nt, file_fig, file_name, onscreen, no_csv, pub, cores):
    """
    Special function to split read count according to number of times aligned
    """

    workers = cores
    work_queue = JoinableQueue()
    processes = []
    mgr = Manager()
    count = 0

    refs = RefSeq()
    refs.load_ref_file(ref_file)

    alignment_dict_1 = mgr.dict()  # header:aligned_sRNAs
    alignment_dict_2 = mgr.dict()

    print(colored("------------------ALIGNING READS------------------\n", 'green'))
    for header, seq in refs:
        work_queue.put((header, seq,))
        count += 1
        if count % 10000 == 0:
            _cdp_split_queue(alignment_dict_1, alignment_dict_2, nt, processes, seq_1, seq_2, work_queue,
                             workers)
    _cdp_split_queue(alignment_dict_1, alignment_dict_2, nt, processes, seq_1, seq_2, work_queue,
                     workers)

    alignment_dict_1 = alignment_dict_1.copy()
    alignment_dict_2 = alignment_dict_2.copy()

    times_align_1 = _cdp_split_times_read_aligns(alignment_dict_1)
    times_align_2 = _cdp_split_times_read_aligns(alignment_dict_2)

    header_split_count_1 = _cdp_split_reads_for_header(alignment_dict_1,
                                                       times_align_1,
                                                       seq_1)
    header_split_count_2 = _cdp_split_reads_for_header(alignment_dict_2,
                                                       times_align_2,
                                                       seq_2)

    counts_by_ref = _cdp_split_header_x_y_counts(header_split_count_1,
                                                 header_split_count_2,
                                                 refs)
    if len(counts_by_ref) == 0:
        print("\nNo reads aligned to any reference sequence. \
        Output files not generated\n")
    else:
        _cdp_output(counts_by_ref, file_fig, file_name, onscreen, no_csv, seq_name_1,
                    seq_name_2, ref_file, nt, pub)


def _cdp_split_queue(alignment_dict_1, alignment_dict_2, nt, processes, seq_1, seq_2, work_queue, workers):
    """

    :param alignment_dict_1:
    :param alignment_dict_2:
    :param nt:
    :param processes:
    :param seq_1:
    :param seq_2:
    :param work_queue:
    :param workers:
    :return:
    """
    for w in range(workers):
        p = Process(target=_cdp_split_worker,
                    args=(work_queue,
                          alignment_dict_1,
                          alignment_dict_2,
                          seq_1,
                          seq_2,
                          nt))
        p.start()
        processes.append(p)
    for p in processes:
        p.join()


def _cdp_split_worker(work_queue, alignment_dict_1, alignment_dict_2, seq_1,
                      seq_2, nt):
    # calc aligned sRNAs for each header, duplicate if necessary

    try:
        while not work_queue.empty():
            single_ref = work_queue.get()
            aligned_reads = _cdp_split_dict_align_reads(seq_1, seq_2, single_ref[1], nt)

            if len(aligned_reads[0]) != 0:
                alignment_dict_1[single_ref[0]] = aligned_reads[0]
            if len(aligned_reads[1]) != 0:
                alignment_dict_2[single_ref[0]] = aligned_reads[1]
    except Exception as e:
        print(e)
    return True





def _cdp_split_dict_align_reads(seq_dict_1, seq_dict_2, ref, nt):
    """
    Returns a dictionary with the number of times a read aligns to single
    reference sequence
    Out --> {read:times_aligned}
    
    """
    count_start = 0
    ref_complement = ref.complement()
    split_alignment_dict_1 = {}  # aligned sRNAs
    split_alignment_dict_2 = {}  # aligned sRNAs

    while count_start < (len(ref) - (nt - 1)):
        query_seq_fwd, query_seq_rvs = _get_query_seqs(count_start, ref, ref_complement, nt)
        _cdp_split_single_align_reads(query_seq_fwd, query_seq_rvs, split_alignment_dict_1, seq_dict_1)
        _cdp_split_single_align_reads(query_seq_fwd, query_seq_rvs, split_alignment_dict_2, seq_dict_2)
        count_start += 1
    return (split_alignment_dict_1, split_alignment_dict_2)


def _cdp_split_single_align_reads(query_seq_fwd, query_seq_rvs, split_alignment_dict, seq_dict):
    """

    :param query_seq_fwd:
    :param query_seq_rvs:
    :param split_alignment_dict:
    :return:
    """
    if query_seq_fwd in seq_dict and query_seq_fwd in split_alignment_dict:
        split_alignment_dict[query_seq_fwd] += 1
    elif query_seq_fwd in seq_dict and query_seq_fwd \
            not in split_alignment_dict:
        split_alignment_dict[query_seq_fwd] = 1
    if query_seq_rvs in seq_dict and query_seq_rvs in split_alignment_dict:
        split_alignment_dict[query_seq_rvs] += 1
    elif query_seq_rvs in seq_dict and query_seq_rvs \
            not in split_alignment_dict:
        split_alignment_dict[query_seq_rvs] = 1


def _cdp_split_times_read_aligns(split_alignment_dict):
    """
    Dict. of times a read aligns to all references
    {read: times aligned} 
    """

    sRNA_align_counts = {}
    for aligned_sRNAs in split_alignment_dict.values():
        for aligned_sRNA, count in aligned_sRNAs.items():
            if aligned_sRNA in sRNA_align_counts:
                sRNA_align_counts[aligned_sRNA] += count
            else:
                sRNA_align_counts[aligned_sRNA] = count
    return sRNA_align_counts


def _cdp_split_reads_for_header(split_align_dict, split_align_count_dict, seq_dict):
    """
    Dict -->Even split read aligned counts, so total reads aligned = read count
    in original seq file
    {header:split_count}
    """

    header_split_count = {}
    for header, sRNA_dict in split_align_dict.items():
        header_split_count[header] = 0
        for sRNA in sRNA_dict:
            header_split_count[header] \
                += ((seq_dict[sRNA] / split_align_count_dict[sRNA]) * split_align_dict[header][sRNA])
    return header_split_count


def _cdp_split_header_x_y_counts(header_split_count_1, header_split_count_2, refs):
    """
    For each header in reference that has > 0 alignments in 1 file
    
    dict --> {header: (split counts 1:split counts 2)}
    """
    # construct x,y counts for each header
    counts_by_ref = {}
    for header in refs.headers():
        if header in header_split_count_1 and header in header_split_count_2:
            counts_by_ref[header] = (header_split_count_1[header],
                                     header_split_count_2[header])
        elif header in header_split_count_1 and header \
                not in header_split_count_2:
            counts_by_ref[header] = (header_split_count_1[header], 0)
        elif header not in header_split_count_1 and header in \
                header_split_count_2:
            counts_by_ref[header] = (0, header_split_count_2[header])
    return counts_by_ref


def _cdp_output(counts_by_ref, file_fig, file_name, onscreen, no_csv, seq_name_1,
                seq_name_2, ref_file, nt, pub):
    """
    Organise csv or pdf output for CDP analysis
    """
    ref_name = ah.single_file_output(ref_file)
    if file_fig or onscreen:

        if file_name == "auto":
            file_name = ah.cdp_file_output(seq_name_1,
                                           seq_name_2,
                                           ref_name,
                                           nt,
                                          "pdf")
        pr.cdp_plot(counts_by_ref,
                    seq_name_1,
                    seq_name_2,
                    nt,
                    onscreen,
                    file_fig,
                    file_name,
                    pub)

    if no_csv:
        out_csv_name = ah.cdp_file_output(seq_name_1,
                                          seq_name_2,
                                          ref_name,
                                          nt,
                                          "csv")

        wtf.cdp_output(counts_by_ref,
                       seq_name_1,
                       seq_name_2,
                       out_csv_name)


def cdp_no_split_single(loaded_seq_list, loaded_seq_name_list,
                        ref_file,
                        nt, cores):
    """
    Aligns a single SRNA_seq object to multiple ref seqs in a Ref object
    at a time.  No splitting of read counts.
    """

    refs = RefSeq()
    refs.load_ref_file(ref_file)
    print(colored("------------------ALIGNING READS------------------\n", 'green'))

    workers = cores
    work_queue = JoinableQueue()
    processes = []
    mgr = Manager()
    count = 0
    counts_by_ref = mgr.dict()  # {header:[count1, count2,.......]}
    for header, seq in refs:
        work_queue.put((header, seq,))
        count += 1
        if count % 10000 == 0:
            _cdp_no_split_single_queue(counts_by_ref, loaded_seq_list, nt, processes, work_queue, workers)
    _cdp_no_split_single_queue(counts_by_ref, loaded_seq_list, nt, processes, work_queue, workers)

    _cdp_single_output(counts_by_ref.copy(), loaded_seq_name_list, ref_file, nt)


def _cdp_no_split_single_queue(counts_by_ref, loaded_seq_list, nt, processes, work_queue, workers):
    """

    :param counts_by_ref:
    :param loaded_seq_list:
    :param nt:
    :param processes:
    :param work_queue:
    :param workers:
    :return:
    """
    for w in range(workers):
        p = Process(target=_cdp_no_split_single_worker, args=(work_queue,
                                                              counts_by_ref,
                                                              loaded_seq_list,
                                                              nt))
        p.start()
        processes.append(p)
    for p in processes:
        p.join()


def _cdp_no_split_single_worker(work_queue, counts_by_ref, loaded_seq_list, nt):
    """
    Worker process - get ref from work queue, aligns reads from all seqs in seq
    list and adds as list of counts to the ref header in the dict  
    """
    try:
        while not work_queue.empty():
            ref = work_queue.get()
            for single_seq in loaded_seq_list:
                aligned_count = _cdp_no_split_count_aligned_reads_to_seq(single_seq, ref[1], nt)
                _cdp_worker_helper(aligned_dict, counts_by_ref, ref)

    except Exception as e:
        print(e)
    return True


def cdp_split_single(loaded_seq_list, loaded_seq_name_list,
                     ref_file,
                     nt, cores):
    """
    Aligns a single SRNA_seq object to multiple ref seqs in a Ref object
    at a time.  Splitting of read counts.
    """

    refs = RefSeq()
    refs.load_ref_file(ref_file)
    print(colored("------------------ALIGNING READS------------------\n", 'green'))

    workers = cores
    work_queue = JoinableQueue()
    processes = []
    mgr = Manager()
    count = 0
    counts_by_ref = mgr.dict()  # {header:[dict, dict2,.......]}
    for header, seq in refs:
        work_queue.put((header, seq,))
        count += 1
        if count % 10000 == 0:
            _cdp_split_single_queue(counts_by_ref, loaded_seq_list, nt, processes, work_queue, workers)
    _cdp_split_single_queue(counts_by_ref, loaded_seq_list, nt, processes, work_queue, workers)
    counts_by_ref = counts_by_ref.copy()

    # compile results
    # [{},{},{}]
    list_of_align_dicts = [{}]
    for i in range(len(loaded_seq_list) - 1):
        list_of_align_dicts.append({})

    # Split the dicts up --> THIS COULD BE DONE BETTER

    for header, list_of_dicts in counts_by_ref.items():
        for i in range(len(list_of_align_dicts)):
            list_of_align_dicts[i][header] = list_of_dicts[i]

    # Process separately then compile
    list_of_processed_dicts = []
    count = 0
    for align_dict in list_of_align_dicts:
        times_align = _cdp_split_times_read_aligns(align_dict)
        header_split_count = _cdp_split_reads_for_header(align_dict,
                                                         times_align,
                                                         loaded_seq_list[count])
        list_of_processed_dicts.append(header_split_count)
        count += 1
    final_dict = {}  # output to csv writer
    for header in list_of_processed_dicts[0]:
        first_dict = True
        for processed_dict in list_of_processed_dicts:
            if first_dict:
                final_dict[header] = [processed_dict[header]]
                first_dict = False
            else:
                final_dict[header].append(processed_dict[header])
    # remove 0 entries
    final_dict = {k: v for k, v in final_dict.items() if v != [0] * len(loaded_seq_list)}

    _cdp_single_output(final_dict, loaded_seq_name_list, ref_file, nt)


def _cdp_split_single_queue(counts_by_ref, loaded_seq_list, nt, processes, work_queue, workers):
    """

    :param counts_by_ref:
    :param loaded_seq_list:
    :param nt:
    :param processes:
    :param work_queue:
    :param workers:
    :return:
    """
    for w in range(workers):
        p = Process(target=_cdp_split_single_worker, args=(work_queue,
                                                           counts_by_ref,
                                                           loaded_seq_list,
                                                           nt))
        p.start()
        processes.append(p)
    for p in processes:
        p.join()


def _cdp_split_single_worker(work_queue, counts_by_ref, loaded_seq_list, nt):
    """
    Worker process - get ref from work queue, aligns reads from all seqs in seq
    list and adds as list of counts to the ref header in the dict  
    """
    try:
        while not work_queue.empty():
            ref = work_queue.get()
            for single_seq in loaded_seq_list:
                aligned_dict = _cdp_split_dict_align_reads(single_seq, ref[1], nt)
                _cdp_worker_helper(aligned_dict, counts_by_ref, ref)

    except Exception as e:
        print(e)
    return True


def _cdp_worker_helper(aligned_dict, counts_by_ref, ref):
    if ref[0] not in counts_by_ref:
        counts_by_ref[ref[0]] = [aligned_dict]
    else:
        new_count_list = counts_by_ref.get(ref[0]) + [aligned_dict]
        counts_by_ref[ref[0]] = new_count_list


def _cdp_split_single_times_read_aligns(split_alignment_dict, pos):
    """
    Dict. of times a read aligns to all references
    {read: times aligned} 
    """

    sRNA_align_counts = {}
    for aligned_sRNAs in list(split_alignment_dict.values())[pos]:
        for aligned_sRNA, count in aligned_sRNAs.items():
            if aligned_sRNA in sRNA_align_counts:
                sRNA_align_counts[aligned_sRNA][pos] += count
            else:
                sRNA_align_counts[aligned_sRNA][pos] = count
    return sRNA_align_counts


def _cdp_single_output(counts_by_ref, loaded_seq_name_list, ref_file, nt):
    """
    Takes counts by ref dict as an imput {header:[count1,count2,...]}
    """
    out_file = "{0}_multiple_file_alignment_{1}.csv".format(ref_file.split("/")[-1], nt)

    wtf.single_cdp_file_output(counts_by_ref, loaded_seq_name_list, out_file)
