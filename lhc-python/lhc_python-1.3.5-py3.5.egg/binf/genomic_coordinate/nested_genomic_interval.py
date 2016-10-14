from .genomic_interval import GenomicInterval
from lhc.binf.sequence.reverse_complement import reverse_complement


class NestedGenomicInterval(GenomicInterval):
    def __init__(self, start, stop, *, chromosome=None, strand='+', data=None):
        super().__init__(start, stop, chromosome=chromosome, strand=strand, data=data)
        self.children = []

    def __len__(self):
        return sum(len(child) for child in self.children)

    # Position functions
    
    def get_abs_pos(self, pos):
        intervals = self.children if self.strand == '+' else reversed(self.children)
        fr = 0
        for interval in intervals:
            length = len(interval)
            if fr <= pos < fr + length:
                return interval.get_abs_pos(pos - fr)
            fr += length
        raise IndexError('relative position {} not contained within {}'.format(pos, self))
    
    def get_rel_pos(self, pos, types=None):
        rel_pos = 0
        intervals = iter(self.children) if self.strand == '+' else reversed(self.children)
        for interval in intervals:
            if types is not None and interval.type not in types:
                continue
            if interval.start <= pos < interval.stop:
                return rel_pos + interval.get_rel_pos(pos)
            rel_pos += len(interval)
        raise IndexError('absolute position {} not contained within {}'.format(pos, self))
    
    # Sequence functions
    
    def get_sub_seq(self, sequence_set):
        res = ''.join(interval.get_sub_seq(sequence_set) for interval in self.children)
        return res if self.strand == '+' else reverse_complement(res)

    def get_5p(self):
        return self.children[0].get_5p() if self.strand == '+' else\
            self.children[-1].get_5p()

    def get_3p(self):
        return self.children[-1].get_3p() if self.strand == '+' else\
            self.children[0].get_3p()
