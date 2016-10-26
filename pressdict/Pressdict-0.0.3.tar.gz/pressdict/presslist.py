import zlib
import json


sentinel = object()


class Presslist(object):
    """List that stores JSON-serializable objects compressed."""

    def __init__(self):
        self.li = []
        self.compress = lambda obj: zlib.compress(json.dumps(obj))
        self.decompress = lambda string: json.loads(zlib.decompress(string))

    def __iter__(self):
        for elem in self.li:
            yield self.decompress(elem)

    def __len__(self):
        return len(self.li)

    def __contains__(self, elem):
        for li_elem in self.li:
            if self.decompress(li_elem) == elem:
                return True
        return False

    def __getitem__(self, i):
        return self.decompress(self.li[i])

    def __getslice__(self, start, stop):
        return map(self.decompress, self.li[start:stop])

    def __setslice__(self, start, stop, values):
        self.li[start:stop] = map(self.compress, values)

    def __delitem__(self, i):
        del self.li[i]

    def __setitem__(self, index, elem):
        self.li[index] = self.compress(elem)

    def append(self, elem):
        return self.li.append(self.compress(elem))

    def count(self, elem):
        c = 0
        for li_elem in self.li:
            if self.decompress(li_elem) == elem:
                c += 1
        return c

    def extend(self, values):
        return self.li.extend(map(self.compress, values))

    def index(self, elem):
        for i, li_elem in enumerate(self.li):
            if self.decompress(li_elem) == elem:
                return i
        raise ValueError("%s is not in Presslist." % elem)

    def pop(self, i=sentinel):
        if i is not sentinel:
            return self.decompress(self.li.pop(i))
        else:
            return self.decompress(self.li.pop())

    def remove(self, elem):
        index = None
        for i, li_elem in enumerate(self.li):
            if self.decompress(li_elem) == elem:
                index = i
                break
        if index is not None:
            del self.li[index]
        else:
            raise ValueError("%s is not in Presslist." % elem)
