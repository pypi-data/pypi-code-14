from collections import namedtuple
from lhc.binf.genomic_feature import GenomicFeature
from lhc.binf.genomic_coordinate import GenomicInterval as Interval


GffLine = namedtuple('GffLine', ('chr', 'source', 'type', 'start', 'stop', 'score', 'strand', 'phase', 'attr'))

GenomicFeatureTracker = namedtuple('GenomicFeatureTracker', ('interval', 'lines'))


class GffLineIterator(object):

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
            res[k] = v.split(',') if ',' in v else v
        return res

    def __getstate__(self):
        return self.iterator, self.line_no

    def __setstate__(self, state):
        self.iterator, self.line_no = state


class GffEntryIterator(object):

    __slots__ = ('it', 'completed_features', 'c_feature', 'c_line', 'c_interval')

    def __init__(self, fname):
        self.it = GffLineIterator(fname)
        self.completed_features = []
        self.c_feature = 0
        line = next(self.it)
        self.c_line = [line]
        self.c_interval = Interval(line.chr, line.start, line.stop)

    def __iter__(self):
        return self

    @property
    def line_no(self):
        return self.it.line_no

    def __next__(self):
        completed_features = self.get_completed_features()
        if self.c_feature >= len(completed_features):
            raise StopIteration
        feature = completed_features[self.c_feature]
        self.c_feature += 1
        return feature

    def get_completed_features(self):
        if self.c_feature < len(self.completed_features):
            return self.completed_features

        self.c_feature = 0
        lines = self.c_line
        for line in self.it:
            if not self.c_interval.overlaps(line):
                self.c_line = [line]
                self.c_interval = Interval(line.chr, line.start, line.stop)
                self.completed_features = self.get_features(lines)
                return self.completed_features
            lines.append(line)
            self.c_interval.union_update(line, compare_strand=False)
        self.c_line = []
        self.c_interval = None
        self.completed_features = self.get_features(lines)
        return self.completed_features

    @staticmethod
    def get_features(lines):
        top_features = {}
        open_features = {}
        for i, line in enumerate(lines):
            id = line.attr.get('ID', str(i))
            ivl = Interval(line.chr, line.start, line.stop, line.strand)
            name = line.attr.get('transcript_id', id).split('.')[0] if line.type in {'mRNA', 'exon', 'transcript'} else\
                line.attr.get('protein_id', id).split('.')[0] if line.type == 'CDS' else\
                line.attr.get('Name', id)
            feature = GenomicFeature(name, line.type, ivl, line.attr)
            if id in open_features:
                feature.children = open_features[id].children
            elif id in top_features:
                feature.children = top_features[id].children
            open_features[id] = feature
            if 'Parent' in line.attr:
                parents = line.attr['Parent'] if isinstance(line.attr['Parent'], list) else [line.attr['Parent']]
                for parent in parents:
                    if parent not in open_features:
                        open_features[parent] = GenomicFeature(parent)
                    open_features[parent].add_child(feature)
            else:
                top_features[id] = feature
        if len(top_features) == 0:
            return []
        return list(zip(*sorted(top_features.items())))[1]

    def __getstate__(self):
        return self.it, self.completed_features, self.c_feature, self.c_line, self.c_interval

    def __setstate__(self, state):
        self.it, self.completed_features, self.c_feature, self.c_line, self.c_interval = state
