"""
Created on 22 Jan 2016

@author: steve
"""
"""
Write alignment results to file (csv format)
"""

import csv


def csv_output(alignment_dict, nt, seq_file_name, header):
    """
    Writes to file in CSV format --> sRNA seq , pos, count
    Single reference alignment - den; single sRNA length
    :param alignment_dict: {sRNA sequence (str): position (int), count(float)} (dict)
    :param nt: aligned read length (int)
    :param seq_file_name: sequence file name (str)
    :param header: reference name (str)

    """

    alignment_list = []

    for sRNA, alignment in alignment_dict:
        for i in alignment:
            alignment_list.append((sRNA, i[0], i[1]))
    alignment_list.sort(key=lambda tup: tup[1])
    with open(header + '_' + seq_file_name + '_' + str(nt) \
                      + '.csv', 'w') as csvfile:
        mycsv = csv.writer(csvfile, delimiter=',')
        mycsv.writerow(['sRNA', '5-prime nuc. position', 'Count'])
        for alignment in alignment_list:
            out = [str(alignment[0]), alignment[1] + 1, alignment[2]]
            mycsv.writerow(out)
    csvfile.close()


def mnt_csv_output(alignment_dict_21, alignment_dict_22, alignment_dict_24,
                   seq_file_name, header):
    """
    Writes to file in CSV format --> sRNA seq , pos, count
    Single reference alignment - mnt3dm; 3 sRNA lengths = 21nt, 22nt and 24nt

    :param alignment_dict_21: {sRNA sequence (str): position (int), count(float)} (dict) - 21 nt alignments
    :param alignment_dict_22: {sRNA sequence (str): position (int), count(float)} (dict) - 22 nt alignments
    :param alignment_dict_24: {sRNA sequence (str): position (int), count(float)} (dict) - 24 nt alignments
    :param seq_file_name: sequence file name (str)
    :param header: reference name (str)
    """
    """
    For mnt - write 3 seperate csvs for 21,22,24 nt sRNA lengths
    """
    csv_output(alignment_dict_21, 21, seq_file_name, header)
    csv_output(alignment_dict_22, 22, seq_file_name, header)
    csv_output(alignment_dict_24, 24, seq_file_name, header)


def cdp_output(counts_by_ref, header1, header2, out_file):
    """
    Writes to file in CSV format --> reference_header, aligned_count_x, aligned_count_y
    Multiple reference alignment - CDP; single sRNA length
    :param counts_by_ref: {reference header (str): aligned_count_x (float), aligned_count_y (float)} (dict)
    :param header1: column header_x (str)
    :param header2: column_header_y (str)
    :param out_file: CSV file name for output (str)
    """
    """
    Write to file --> csv
    sRNA, seq1_count, seq2_count
    """
    results_list = []
    for header, counts in counts_by_ref.items():
        results_list.append((header, counts[0], counts[1]))
    with open(out_file, 'w') as csvfile:
        mycsv = csv.writer(csvfile, delimiter=',')
        mycsv.writerow(['', header1, header2])
        for result in results_list:
            out = [result[0], result[1], result[2]]
            mycsv.writerow(out)

    csvfile.close()


def single_cdp_file_output(counts_by_ref, loaded_seq_name_list, out_file):
    """
    Writes to file in CSV format --> reference_header, aligned_count_1, aligned_count_2,.......
    Multiple reference alignment - single CDP; single sRNA length, multiple sequences
    :param counts_by_ref: {reference header (str): seq_1 aligned count (float), seq 2 aligned count (float), .....}
    (dict)
    :param loaded_seq_name_list: [seq_1 name (str), seq_2 name (str),....] (list)
    :param out_file: CSV file name for output (str)
    """
    """
    csv output for sinlge CDP alignments
    

    Each row is a ref seq header
    
    header, seq1, seq2 etc)
    """

    first_row = ["Reference"] + loaded_seq_name_list
    with open(out_file, 'w') as csvfile:
        mycsv = csv.writer(csvfile, delimiter=',')
        mycsv.writerow(first_row)

        for header, counts in counts_by_ref.items():
            out = [header] + counts
            mycsv.writerow(out)
    csvfile.close()
