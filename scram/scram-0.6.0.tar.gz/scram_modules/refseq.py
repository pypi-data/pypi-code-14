import time
from dna import DNA
from termcolor import colored


class RefSeq(object):
    """
    A class for reference sequences  - stores header:seq pairs in a dictionary

    {header:seq}
    """

    def __init__(self):
        self._internal_dict = {}  # internal dictionary for class

    def __setitem__(self, header, sequence):
        self._internal_dict[header] = sequence  # {header:sequence (DNA)}

    def __getitem__(self, header):
        return self._internal_dict[header]  # get DNA sequence for header

    def __iter__(self):
        return iter(self._internal_dict.items())  # iterable

    def __len__(self):
        return len(self._internal_dict)  # number of ref seqs in object

    def headers(self):
        return self._internal_dict.keys()  # view of headers

    def sequences(self):
        return self._internal_dict.values()  # view of DNA sequences

    def load_ref_file(self, ref_file):
        """
        Load reference file in FASTA format

        :param ref_file: /path/to/ref/file
        """
        print(colored("\n-----------------LOADING REFERENCE----------------", 'green'))
        start = time.clock()
        # ref_dict = {}
        ref_count = 0
        loaded_ref = open(ref_file, 'r')
        full_len_seq = ''
        key = ''
        first_header = True
        for line in loaded_ref:
            if line[0] == '>' and full_len_seq == '':
                key = line.strip()
                ref_count += 1
                if first_header:
                    first_header = False
            elif line[0] == '>' and full_len_seq != '':
                self._internal_dict.update({key: DNA(full_len_seq)})
                key = line.strip()
                full_len_seq = ''
                ref_count += 1
            elif line[0] == '' and full_len_seq != '':
                self._internal_dict.update({key: DNA(full_len_seq)})
                key = line.strip()
                full_len_seq = ''
            elif line[0] == '':
                pass
            else:
                full_len_seq += line.strip().upper()

        self._internal_dict.update({key: DNA(full_len_seq)})

        print('\n----{0} reference sequences loaded for alignment----'.format(ref_count))
        if len(self._internal_dict) == 1:
            print("\n{0} length = {1} bp".format(ref_file.split('/')[-1], len(full_len_seq)))
        print("\nReference sequence loading time = " + str((time.clock() - start)) + " seconds\n")
