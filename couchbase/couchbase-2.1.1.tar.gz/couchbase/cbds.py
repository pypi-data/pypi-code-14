from couchbase.bucket import Bucket
import couchbase.exceptions as E
import couchbase.subdocument as SD


class CollectionBase(object):
    def __init__(self, docid, bucket):
        # type: (str, Bucket) -> None
        self._bucket = bucket
        self._docid = docid
        # self._create = create
        try:
            bucket.insert(docid, self._deflcls())
        except E.KeyExistsError:
            pass

    def _len46(self):
        try:
            res = self._bucket.lookup_in(self._docid, SD.get_count(''))
            return res[0]
        except E.NotFoundError:
            return 0

    def _len45(self):
        try:
            res = self._bucket.get(self._docid)
            return len(res.value)
        except E.NotFoundError:
            return 0

    def __len__(self):
        return self._len45()

    def __contains__(self, item):
        # Get the actual list:
        doc = self._bucket.get(self.__doc__).value
        return item in doc

    def __nonzero__(self):
        return not len(self)


class Dict(CollectionBase):
    def __getitem__(self, item):
        try:
            return self._bucket.lookup_in(self._docid, SD.get(item))[0]
        except E.SubdocPathNotFoundError:
            raise IndexError(item)
        except E.NotFoundError:
            pass

    def __setitem__(self, key, value):
        self._bucket.mutate_in(
            self._docid, SD.upsert(key, value))

    def __delitem__(self, item):
        try:
            self._bucket.mutate_in(self._docid, SD.remove(item))
        except E.SubdocPathNotFoundError:
            raise IndexError(item)
        except E.NotFoundError:
            pass

    def __iter__(self):
        doc = self._bucket.get(self._docid).value
        return iter(doc.items())

    def _deflcls(self):
        return {}


class List(CollectionBase):
    def insert(self, ix, value):
        self._bucket.mutate_in(self._docid, SD.array_insert(ix, value))

    def __getitem__(self, item):
        return self._bucket.lookup_in(self._docid, SD.get('[{0}]'.format(item)))[0]

    def __setitem__(self, key, value):
        self._bucket.mutate_in(self._docid, SD.array_insert('[{0}]'.format(key), value))

    def append(self, value):
        self._bucket.mutate_in(self._docid, SD.array_append('', value))

    def extend(self, l2):
        self._bucket.mutate_in(self._docid, SD.array_append('', *l2))

    def pop(self, index=-1):
        ixstr = '[{0}]'.format(index)
        while True:
            try:
                rv = self._bucket.lookup_in(self._docid, SD.get(ixstr))
                val = rv[0]
                self._bucket.mutate_in(self._docid, SD.remove(ixstr), cas=rv.cas)
                return val
            except E.KeyExistsError:
                continue

    def _deflcls(self):
        return []


class Set(CollectionBase):
    def _deflcls(self):
        return []

    def add(self, item):
        if not isinstance(item, (int, str, bool, None)):
            raise ValueError('Invalid type!')
        try:
            self._bucket.mutate_in(
                self._docid, SD.array_addunique('', item))
        except E.SubdocPathExistsError:
            pass

    def remove(self, item):
        # Slow!
        while True:
            rv = self._bucket.get(self._docid)
            # Find the index of the item
            try:
                ix = rv.value.index(item)
            except ValueError:
                return
            try:
                ixstr = '[{0}]'.format(ix)
                self._bucket.mutate_in(self._docid,
                                       SD.remove(ixstr), cas=rv.cas)
                return
            except E.KeyExistsError:
                pass


class Queue(List):
    def push(self, *items):
        self.extend(items)


if __name__ == "__main__":
    cb = Bucket('couchbase://localhost/default')

    cb.remove('a_map', quiet=True)
    dd = Dict('a_map', cb)
    dd['foo'] = 'bar'
    print(cb.get('a_map'))


    cb.remove('a_list', quiet=True)
    aa = List('a_list', cb)
    aa.append('Hello')
    aa.append('World')
    aa.extend(['foo', 'bar', 'baz'])
    print(cb.get('a_list'))

    cb.remove('a_set', quiet=True)
    ss = Set('a_set', cb)
    ss.add('hello')
    ss.add('hello')
    print(len(ss))
    ss.remove('hello')
    print(len(ss))

    cb.remove('a_queue', quiet=True)
    qq = Queue('a_queue', cb)
    qq.push(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
    print(qq.pop())
    print(qq.pop())

    cb.queue_pop()