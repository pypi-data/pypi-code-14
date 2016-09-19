from .inorder_access_set import FastaInOrderAccessSet
from .iterator import FastaIterator


def iter_fasta(iterator):
    """
    A generator to iterate over fasta files

    :param iterator: iterator over fasta file lines
    :type iterator: Iterable
    :return: fasta entries
    :rtype: tuple
    """
    hdr = next(iterator)
    seq = []
    while not hdr.startswith('>'):
        hdr = next(iterator)
    for line in iterator:
        if line.startswith('>'):
            yield hdr[1:].strip(), ''.join(seq)
            hdr = line
            seq = []
        else:
            seq.append(line.strip())
    yield hdr[1:].strip(), ''.join(seq)
