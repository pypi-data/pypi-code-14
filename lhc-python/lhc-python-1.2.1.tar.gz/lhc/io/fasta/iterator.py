from collections import namedtuple


FastaLine = namedtuple('FastaLine', ('hdr', 'seq', 'start', 'stop'))


class FastaIterator(object):
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
