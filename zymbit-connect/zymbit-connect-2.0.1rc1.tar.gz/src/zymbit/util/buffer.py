import collections


class BufferIterator(collections.Iterable):
    def __init__(self, buf=None, split_at='\n'):
        self.buf = ''
        if buf:
            self.write(buf)

        self.split_at = split_at

    def __iter__(self):
        return self

    def __next__(self):
        try:
            idx = self.buf.index(self.split_at)
        except ValueError:
            raise StopIteration()

        buf = self.buf[:idx+1]
        self.buf = self.buf[idx+1:]

        return buf

    def write(self, buf):
        try:
            buf = buf.decode('utf8')
        except AttributeError:
            pass

        self.buf += buf
