_REVCMP = bytes.maketrans(b'acgtuwrkysmbhdvnACGTUWRKYSMBHDVN', b'tgcaawymrskvdhbnTGCAAWYMRSKVDHBN')


def revcmp(seq):
    return seq.translate(_REVCMP)[::-1]
