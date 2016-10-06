import gzip

from lhc.io.vcf.iterator import VcfIterator, Variant, get_float, get_samples


class IndexedVcfFile(object):
    def __init__(self, fname, index):
        self.index = index
        self.it = VcfIterator(gzip.open(fname) if fname.endswith('gz') else open(fname))

    def fetch(self, chr, start, stop=None):
        if stop is None:
            stop = start + 1
        return [self.get_variant(line.rstrip('\r\n').split('\t')) for line in self.index.fetch(chr, start, stop)]

    def get_variant(self, parts):
        info = dict(i.split('=', 1) if '=' in i else (i, i) for i in parts[7].split(';'))
        format = None if len(parts) < 9 else parts[8].split(':')
        return Variant(
            (parts[0], int(parts[1]) - 1),
            parts[2],
            parts[3],
            parts[4].split(','),
            get_float(parts[5]),
            set(parts[6].split(',')),
            info,
            format,
            get_samples(self.it.samples, parts[9:], format)
        )
