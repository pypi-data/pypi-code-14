import operator

from dna import DNA


class AlignedReads(object):
    """
    Class for aligning reads of a discrete size to a reference sequence
    """

    def __init__(self):
        self._internal_dict = {}  # Store alignment as internal dict to class

    def __setitem__(self, sRNA, alignment):
        """

        :param sRNA: read sequence (DNA)
        :param alignment: [[position, read count],......] list(list(int, float),.....)
        :return:
        """
        self._internal_dict[sRNA] = alignment

    def __getitem__(self, sRNA):
        return self._internal_dict[sRNA] # Return alignments for a read

    def __iter__(self):
        return iter(self._internal_dict.items()) #iterable

    def __len__(self):
        return len(self._internal_dict) #number of reads aligned (int)

    def sRNAs(self):
        return self._internal_dict.keys() #view of reads aligned

    def alignments(self):
        return self._internal_dict.values() #view of alignments

    def align_reads_to_ref(self, seq_dict, ref, nt):
        """
        Align reads from SRNASeq object to reference in RefSeq object
        :param seq_dict: SRNASeq object
        :param ref: RefSeq object
        :param nt: read length to align (int)
        """
        count_start = 0

        ref_complement = ref.complement()

        while count_start < (len(ref) - (nt - 1)):
            query_seq_fwd = DNA(ref[count_start:(count_start + nt)])
            query_seq_rvs = DNA(ref_complement[count_start:(count_start + nt)])
            if query_seq_fwd in seq_dict and query_seq_fwd not in self._internal_dict:
                self._internal_dict[query_seq_fwd] = [
                    [count_start, seq_dict[query_seq_fwd]]]
            elif query_seq_fwd in seq_dict and query_seq_fwd in self._internal_dict:
                self._internal_dict[query_seq_fwd].append(
                    [count_start, seq_dict[query_seq_fwd]])
            if query_seq_rvs in seq_dict and query_seq_rvs not in self._internal_dict:
                self._internal_dict[query_seq_rvs] = [
                    [len(ref) - count_start - 1, 0 - seq_dict[query_seq_rvs]]]
            elif query_seq_rvs in seq_dict and query_seq_rvs in self._internal_dict:
                self._internal_dict[query_seq_rvs].append(
                    [len(ref) - count_start - 1, 0 - seq_dict[query_seq_rvs]])
            count_start += 1

    def split(self):
        """
        Divide the aligned read count at each position by the number of times the read aligns
        """
        for alignments in list(self._internal_dict.values()):
            for alignment in alignments:
                alignment[1] /= len(alignments)

    def aln_by_ref_pos(self, nt):
        """
        Returns two sorted lists of (pos,count) tuples - fwd and rvs.  For plotting.  sRNA seq not tracked
        :param nt: length of aligned reads
        :return: [sorted list of sense alignments (sorted by position),
        sorted list of sense alignments (sorted by position), no of reads aligned (float)
        """

        fwd_alignment = {}
        rvs_alignment = {}
        aln_count = 0
        for alignment in self._internal_dict.values():
            for i in alignment:
                if i[1] > 0:
                    fwd_alignment[i[0]] = i[1]  # {pos:count}
                    aln_count += i[1]
                elif i[1] < 0:
                    rvs_alignment[i[0]] = i[1]  # {pos:count}

                    aln_count -= i[1]

        sorted_fwd_alignment = sorted(list(fwd_alignment.items()),
                                      key=operator.itemgetter(0))

        sorted_rvs_alignment = sorted(list(rvs_alignment.items()),
                                      key=operator.itemgetter(0))

        print("\n{0} {1} nt reads per million reads have aligned\n".format(aln_count, nt))
        print("-" * 50)
        return [sorted_fwd_alignment, sorted_rvs_alignment, aln_count]
