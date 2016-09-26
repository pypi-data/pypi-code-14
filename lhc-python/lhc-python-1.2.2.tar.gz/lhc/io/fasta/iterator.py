from collections import namedtuple


class FastaIterator:

    __slots__ = ('iterator', 'header', 'sequence')

    def __init__(self, iterator):
        self.iterator = iterator
        self.header = next(iterator).rstrip('\r\n')[1:]
        self.sequence = []

    def __iter__(self):
        return self

    def __next__(self):
        header = self.header
        if header is None:
            raise StopIteration

        sequence = self.sequence
        for line in self.iterator:
            if line.startswith('>'):
                self.header = line.rstrip('\r\n')[1:]
                self.sequence = []
                return header, ''.join(sequence)
            else:
                sequence.append(line.rstrip('\r\n'))
        self.header = None
        return header, ''.join(sequence)

    def __getstate__(self):
        return self.iterator, self.header, self.sequence

    def __setstate__(self, state):
        self.iterator, self.header, self.sequence = state


FastaLine = namedtuple('FastaLine', ('hdr', 'seq', 'start', 'stop'))


class FastaLongLineIterator(object):
    """
    A fasta iterator that puts a limit on the line size (some fasta files put the entire genome on one line). Headers
    retain full length.
    """
    def __init__(self, fileobj, threshold=2**16):
        self.fileobj = fileobj
        self.threshold = threshold
        self.hdr = None
        self.pos = 0

    def __iter__(self):
        return self

    def __next__(self):
        line = self.fileobj.readline(self.threshold)
        while line == '\n':
            line = self.fileobj.readline(self.threshold)
        if line.startswith('>'):
            if not line.endswith('\n'):
                line += self.fileobj.readline()
            self.hdr = line.strip()
            self.pos = 0
            line = self.fileobj.readline(self.threshold)
            while line == '\n':
                line = self.fileobj.readline(self.threshold)
        line = line.strip()
        res = FastaLine(self.hdr, line.strip(), self.pos, self.pos + len(line))
        self.pos += len(line)
        return res
