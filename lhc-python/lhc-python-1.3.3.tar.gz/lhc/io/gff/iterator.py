from collections import namedtuple
from lhc.binf.genomic_coordinate import NestedGenomicInterval as Interval
from lhc.binf.genomic_coordinate.nested_genomic_interval_factory import NestedGenomicIntervalFactory


GffLine = namedtuple('GffLine', ('chr', 'source', 'type', 'start', 'stop', 'score', 'strand', 'phase', 'attr'))


class GffLineIterator:

    __slots__ = ('iterator', 'line_no')

    def __init__(self, iterator):
        self.iterator = iterator
        self.line_no = 0

    def __iter__(self):
        return self

    def __next__(self):
        while True:
            line = self.parse_line(next(self.iterator))
            self.line_no += 1
            if line.type != 'chromosome':
                break
        return line

    @staticmethod
    def parse_line(line):
        parts = line.rstrip('\r\n').split('\t')
        parts[3] = int(parts[3]) - 1
        parts[4] = int(parts[4])
        parts[8] = GffLineIterator.parse_attributes(parts[8])
        return GffLine(*parts)

    @staticmethod
    def parse_attributes(attr):
        res = {}
        for part in attr.split(';'):
            if part == '':
                continue
            k, v = part.split('=', 1) if '=' in part else part
            res[k] = v.split(',')
        return res

    def __getstate__(self):
        return self.iterator, self.line_no

    def __setstate__(self, state):
        self.iterator, self.line_no = state


class GffIterator:

    __slots__ = ('iterator', 'factory')

    def __init__(self, iterator):
        self.iterator = iterator
        self.factory = NestedGenomicIntervalFactory()

        line = next(self.iterator)
        self.factory.add_interval(_get_interval(line, 0), parents=_get_parent(line))

    def __iter__(self):
        return self

    def __next__(self):
        if self.factory.drained():
            raise StopIteration

        try:
            while not self.factory.has_complete_interval():
                line = next(self.iterator)
                self.factory.add_interval(_get_interval(line, self.iterator.line_no), parents=_get_parent(line))
        except StopIteration:
            self.factory.close()

        return self.factory.get_complete_interval()

    def __getstate__(self):
        return self.iterator, self.factory

    def __setstate__(self, state):
        self.iterator, self.factory = state


def _get_interval(line, line_no):
    name = _get_name(line, default_id=str(line_no))
    data = {'type': line.type, 'attr': line.attr, 'name': name}
    return Interval(line.start, line.stop, chromosome=line.chr, strand=line.strand, data=data)


def _get_name(line, *, default_id=None):
    id = line.attr.get('ID', default_id)
    name = line.attr.get('transcript_id', id)[0] if line.type in {'mRNA', 'exon', 'transcript'} else \
        line.attr.get('protein_id', id)[0] if line.type == 'CDS' else \
        line.attr.get('ID', id)[0] if line.type == 'protein' else \
        line.attr.get('Name', id)[0]
    return name


def _get_parent(line):
    if 'Parent' in line.attr:
        return line.attr.get('Parent')
