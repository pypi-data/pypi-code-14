from collections import namedtuple
from itertools import chain
from lhc.binf.genomic_coordinate import GenomicInterval as Interval


BedLine = namedtuple('BedLine', ('chr', 'start', 'stop', 'name', 'score', 'strand'))
BedEntry = namedtuple('BedEntry', ('ivl', 'name', 'score'))


class BedLineIterator(object):
    def __init__(self, iterator):
        self.iterator = iterator
        self.line_no = 0
        self.hdrs = self.parse_headers()
    
    def __del__(self):
        self.close()
    
    def __iter__(self):
        return self
    
    def __next__(self):
        line = next(self.iterator)
        self.line_no += 1
        if line == '':
            return
        return self.parse_line(line)

    def seek(self, fpos):
        self.iterator.seek(fpos)

    def close(self):
        if hasattr(self.iterator, 'close'):
            self.iterator.close()

    def parse_headers(self):
        hdrs = []
        line = next(self.iterator)
        line_no = 1
        while line[:5] in {'brows', 'track'}:
            line = next(self.iterator)
            line_no += 1
        self.iterator = chain([line], self.iterator)
        self.line_no = line_no
        return hdrs

    @staticmethod
    def parse_line(line):
        parts = line.rstrip('\r\n').split('\t')
        parts[1] = int(parts[1]) - 1
        parts[2] = int(parts[2])
        parts.extend(None for i in range(6 - len(parts)))
        return BedLine(*parts)


class BedEntryIterator(BedLineIterator):
    def __init__(self, iterator):
        super().__init__(iterator)

    def __next__(self):
        line = next(self.iterator)
        self.line_no += 1
        if line == '':
            return()
        return self.parse_entry(self.parse_line(line))

    @staticmethod
    def parse_entry(line):
        return BedEntry(Interval(line.start, line.stop, chromosome=line.chr, strand=line.strand), line.name, line.score)
