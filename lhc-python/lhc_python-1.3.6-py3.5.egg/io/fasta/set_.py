class FastaSet(object):
    def __init__(self, iterator):
        self.data = {k.split()[0]: v for k, v in iterator}

    def __getitem__(self, key):
        if isinstance(key, str):
            return self.data[key]
        elif hasattr(key, 'chromosome') and hasattr(key, 'position'):
            return self.data[key.chromosome][key.position]
        elif hasattr(key, 'chromosome') and hasattr(key, 'start') and hasattr(key, 'stop'):
            return self.data[key.chromosome][key.start.position:key.stop.position]
        raise NotImplementedError('Fasta set random access not implemented for {}'.format(type(key)))

    def fetch(self, chr, start, stop):
        return self.data[chr][start:stop]
