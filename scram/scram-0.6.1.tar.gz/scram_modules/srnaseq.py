'''
Small RNA storage class

Stores unique sequence and read count in an internal dictionary.  
Automatic normalisation to RPMR once loaded from file
'''

from dna import DNA
import time


class SRNASeq(object):
    def __init__(self):
        self._internal_dict = {}  # internal dictionary for class

    def __setitem__(self, sequence, count):
        self._internal_dict[sequence] = count  # {sequence:count}

    def __getitem__(self, sequence):
        return self._internal_dict[sequence]  # get count for sequence

    def __iter__(self):
        return iter(self._internal_dict.items())  # iterable

    def __len__(self):
        return len(self._internal_dict)  # number of sequences stored

    def __contains__(self, sequence):
        return sequence in self._internal_dict  # true if sequence stored

    def sRNAs(self):
        return self._internal_dict.keys()  # returns a view of all sequences

    def counts(self):
        return self._internal_dict.values()  # returns a view all counts

    def load_seq_file(self, seq_file, sRNA_max_len_cutoff, min_reads, sRNA_min_len_cutoff):
        """
        Load collapsed FASTA  sequence file
            eg. >1-43456
                AAAAAAATTTTTATATATATA

        Calculate RPMR and apply in  function

        :param seq_file: path/to/seq/file (str)
        :param sRNA_max_len_cutoff: only reads  of length <= sRNA_max_len_cutoff loaded (int)
        :param min_reads: only reads >= min_reads count loaded (int)
        :param sRNA_min_len_cutoff: only reads  of length >= sRNA_min_len_cutoff loaded (int)

        """
        start = time.clock()
        _seq_dict = {}
        read_count = self._single_seq_file_load(_seq_dict, min_reads, sRNA_max_len_cutoff, sRNA_min_len_cutoff,
                                                seq_file)

        # final RPMR - could simplify in future
        for sRNA, count in _seq_dict.items():
            self._internal_dict[sRNA] = count * (float(1000000) / read_count)
        print("\n{0} load time = {1} seconds for {2} reads".format(seq_file.split('/')[-1],
                                                                   str((time.clock() - start)), read_count))
        print("-" * 50)

    def load_seq_file_arg_list(self, seq_file_arg_list, sRNA_max_len_cutoff,
                               min_reads, sRNA_min_len_cutoff):
        """
        Load collapsed FASTA  sequence files from the list - generate single SRNA_seq object with mean

            eg. >1-43456
                AAAAAAATTTTTATATATATA

        Calculate RPMR and apply in  function

        :param seq_file_arg_list: list of seq_file Paths [path/to/seq/file (str),.....] (list)
        :param sRNA_max_len_cutoff: only reads  of length <= sRNA_max_len_cutoff loaded (int)
        :param min_reads: only reads >= min_reads count loaded (int)
        :param sRNA_min_len_cutoff: only reads  of length >= sRNA_min_len_cutoff loaded (int)

        """
        start = time.clock()

        # read_count_1 = 0
        indv_seq_dict_list = []  # list of individual seq_dics
        indv_seq_dict_list_factor = []  # RPMR for each seq. disc

        for seq_file in seq_file_arg_list:
            single_start = time.clock()
            _seq_dict = {}
            read_count = self._single_seq_file_load(_seq_dict, min_reads, sRNA_max_len_cutoff, sRNA_min_len_cutoff,
                                                    seq_file)

            indv_seq_dict_list.append(_seq_dict)
            indv_seq_dict_list_factor.append(float(1000000) / read_count)
            print("\n{0} load time = {1} seconds for {2} reads".format(seq_file.split('/')[-1],
                                                                       str((time.clock() - single_start)), read_count))
        for sRNA, count in indv_seq_dict_list[0].items():
            if all(sRNA in d for d in indv_seq_dict_list):
                total_count = 0
                for i in range(len(indv_seq_dict_list)):
                    total_count += (indv_seq_dict_list[i][sRNA] * indv_seq_dict_list_factor[i])

                self._internal_dict[sRNA] = total_count / len(indv_seq_dict_list)

        print("\nTotal sequence file processing time = " \
              + str((time.clock() - start)) + " seconds\n")
        print("-" * 50)

    def _single_seq_file_load(self, _seq_dict, min_reads, sRNA_max_len_cutoff, sRNA_min_len_cutoff, seq_file):
        """
        Internal class function for a single seq file load.  No normalisation.
        :param _seq_dict: class internal dict for loading collapsed fasta file {sRNA;count} (dict)
        :param min_reads: only reads >= min_reads count loaded (int)
        :param sRNA_max_len_cutoff: only reads  of length <= sRNA_max_len_cutoff loaded (int)
        :param sRNA_min_len_cutoff: only reads  of length >= sRNA_min_len_cutoff loaded (int)
        :param seq_file: path/to/seq/file (str)
        :return: total read count for the file (inside of cutoffs) (int)
        """
        read_count = 0
        with open(seq_file, 'r') as loaded_seq:
            next_line = False
            for line in loaded_seq:
                line = line.strip()
                if line[0] == '>':
                    count = int(line.split('-')[1])
                    next_line = True
                elif count >= min_reads and sRNA_min_len_cutoff <= len(line) <= sRNA_max_len_cutoff and next_line:
                    _seq_dict[DNA(line)] = count
                    read_count += count
                    next_line = False
                else:
                    pass
        loaded_seq.close()
        return read_count