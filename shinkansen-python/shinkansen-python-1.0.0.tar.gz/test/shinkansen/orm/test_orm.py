import collections
import functools

import mox
import retrying

from shinkansen import config, lock, orm


class TestException(Exception):
    pass


class TestORM(mox.MoxTestBase):
    def test_retry(self):
        a = [1, 2]
        k = {'a': 3, 'b': 4, 'cc': 5}

        self.mox.StubOutWithMock(retrying, 'retry')
        retrying.retry(
            *a,
            retry_on_exception=mox.IgnoreArg(),
            wait_random_min=mox.IgnoreArg(),
            wait_random_max=mox.IgnoreArg(),
            **k
        ).AndReturn(lambda func: func)
        func = self.mox.CreateMockAnything()
        self.mox.StubOutWithMock(functools, 'wraps')
        functools.wraps(func).AndReturn(lambda func: func)
        func()
        self.mox.ReplayAll()
        orm.retry(*a, **k)(func)()

    def test_raise_redis_exceptions_no_results(self):
        self.assertEqual(orm.raise_redis_exceptions([]), [])

    def test_raise_redis_exceptions_no_exceptions(self):
        self.assertEqual(orm.raise_redis_exceptions([1, 2, 3]), [1, 2, 3])

    def test_raise_redis_exceptions_single_exception(self):
        with self.assertRaises(TestException):
            orm.raise_redis_exceptions([TestException()])

    def test_raise_redis_exceptions_single_exception_and_results(self):
        with self.assertRaises(TestException):
            orm.raise_redis_exceptions([None, TestException(), 4, 5])

    def test_raise_redis_exceptions_multiple_exception(self):
        exceptions = [TestException('a'), TestException('b')]
        with self.assertRaises(orm.MultiRedisError):
            try:
                orm.raise_redis_exceptions(exceptions)
            except orm.MultiRedisError, e:
                # mark 2 more lines as covered :p
                repr(e)
                str(e)
                self.assertEqual(e.exceptions, exceptions)
                raise


class TestDO(orm.DataObject):
    _key_cols = ['k', 'v']
    _update_cols = ['a', 'b', 'c']
    _tablename = 'TEST'
    _indexes = [['a'], ['a', 'b']]

    def __init__(self, redis):
        super(TestDO, self).__init__(redis)
        self._b = None
        self.a = None
        self.b = None
        self.c = None
        self.k = None
        self.v = None


class TestDataObject(mox.MoxTestBase):
    def setUp(self):
        super(TestDataObject, self).setUp()
        self.orig_QUEUE_SYSTEM = config.QUEUE_SYSTEM
        config.QUEUE_SYSTEM = 'multiprocessing'
        orm.RETRY_ON_EXCEPTION = False

    def tearDown(self):
        config.QUEUE_SYSTEM = self.orig_QUEUE_SYSTEM

    def context(self, val=None):
        ctx = self.mox.CreateMockAnything()
        ctx.__enter__().AndReturn(val)
        ctx.__exit__(mox.IgnoreArg(), mox.IgnoreArg(), mox.IgnoreArg())
        return ctx

    def test_setattr_internal(self):
        do = TestDO(None)
        do._b = 2
        self.assertEqual(do._dirty_fields, set())
        self.assertEqual(do._dirty_indexes, {})

    def test_setattr_public(self):
        do = TestDO(None)
        do.a = 1
        self.assertEqual(do._dirty_fields, set('a'))
        self.assertEqual(do._dirty_indexes, {'TestDO|idx|a': {'a': None}, 'TestDO|idx|a:b': {'a': None, 'b': None}})

    def test_setattr_dirty_index_keeps_first_value(self):
        do = TestDO(None)
        do.a = 1
        do.a = 2
        self.assertEqual(do._dirty_fields, set('a'))
        self.assertEqual(do._dirty_indexes, {'TestDO|idx|a': {'a': None}, 'TestDO|idx|a:b': {'a': None, 'b': None}})

    def test_index_name(self):
        self.assertEqual(TestDO._index_name(['b', 'a']), 'TestDO|idx|a:b')

    def test_key(self):
        do = TestDO(None)
        do.k = 'st'
        do.v = 1234
        self.assertEqual(do._key(), 'TestDO|rec|k=st:v=1234')

    def test_lock(self):
        conn = self.mox.CreateMockAnything()
        do = TestDO(conn)
        do.k = 'st'
        do.v = 1234
        l = self.mox.CreateMockAnything()
        self.mox.StubOutWithMock(lock, 'ReentrantMemLock')
        lock.ReentrantMemLock(do._key() + '.LOCK').AndReturn(l)
        self.mox.ReplayAll()
        self.assertEqual(do._lock(), l)

    def test_lock_key(self):
        conn = self.mox.CreateMockAnything()
        do = TestDO(conn)
        do.k = 'st'
        do.v = 1234
        l = self.mox.CreateMockAnything()
        self.mox.StubOutWithMock(lock, 'ReentrantMemLock')
        key = 'abc4213'
        lock.ReentrantMemLock(key + '.LOCK').AndReturn(l)
        self.mox.ReplayAll()
        self.assertEqual(do._lock(key), l)

    def test_index_key_values(self):
        do = TestDO(None)
        do.a = 42
        do.b = 'gg'
        self.assertEqual(
            do._index_key_values(do._index_name(do._indexes[0]), {'a': 43, 'b': 'hh'}),
            'TestDO|idx|a=43')
        self.assertEqual(
            do._index_key_values(do._index_name(do._indexes[1]), {'a': 43, 'b': 'hh'}),
            'TestDO|idx|a:b=43,hh')

    def test_index_key(self):
        do = TestDO(None)
        do.a = 42
        do.b = 'gg'
        self.assertEqual(
            do._index_key(do._index_name(do._indexes[0])),
            'TestDO|idx|a=42')
        self.assertEqual(
            do._index_key(do._index_name(do._indexes[1])),
            'TestDO|idx|a:b=42,gg')

    def test_as_dict(self):
        do = TestDO(None)
        do.a = 42
        do.b = 'gg'
        do.k = 3
        self.assertEqual(do.as_dict(), {'a': 42, 'b': 'gg', 'k': 3})

    def test_from_dict(self):
        do = TestDO(None)
        # column types default to str
        do.a = '1'
        do.b = '2'
        self.assertEqual(TestDO.from_dict(None, {'a': 1, 'b': 2}), do)

    def test_insert_redis_existing_record(self):
        conn = self.mox.CreateMockAnything()
        do = TestDO(conn)
        do.a = 42
        do.b = 'gg'
        do.k = 3
        do.v = 7
        lock = self.context()
        conn.exists(do._key()).AndReturn(True)
        self.mox.ReplayAll()

        with self.assertRaises(orm.ORMException):
            do.insert(lock=lock)

    def test_insert_redis(self):
        conn = self.mox.CreateMockAnything()
        do = TestDO(conn)
        do.a = 42
        do.b = 'gg'
        do.k = 3
        do.v = 7
        lock = self.context()
        conn.exists(do._key()).AndReturn(False)
        pipe = self.mox.CreateMockAnything()
        conn.pipeline().AndReturn(self.context(pipe))
        pipe.hmset(do._key(), do.as_dict())
        index_name = do._index_map.keys()[0]
        pipe.sadd(do._index_key(index_name), do._key())
        pipe.sadd(index_name, do._index_key(index_name))
        index_name = do._index_map.keys()[1]
        pipe.sadd(do._index_key(index_name), do._key())
        pipe.sadd(index_name, do._index_key(index_name))
        pipe.sadd(do._table_records_key, do._key())
        pipe.execute().AndReturn([])
        self.mox.ReplayAll()

        do.insert(lock=lock)

    def test_update_redis(self):
        conn = self.mox.CreateMockAnything()
        do = TestDO(conn)
        do.a = 42
        do.b = 'gg'
        do.c = 'oh'
        do.k = 3
        do.v = 7
        do._dirty_fields = set()
        do._dirty_indexes = {}
        do.a = 13
        do.b = 'hi'
        do.c = None
        # Converting this into a sorted OrderedDict so that the calls below are in the right order
        do._dirty_indexes = collections.OrderedDict(sorted(do._dirty_indexes.items()))
        lock = self.context()
        pipe = self.mox.CreateMockAnything()
        conn.pipeline().AndReturn(self.context(pipe))
        pipe.hdel(do._key(), 'c')
        pipe.hmset(do._key(), {'a': 13, 'b': 'hi'})
        pipe.smove('TestDO|idx|a=42', 'TestDO|idx|a=13', do._key())
        pipe.sadd('TestDO|idx|a', 'TestDO|idx|a=13')
        pipe.smove('TestDO|idx|a:b=42,gg', 'TestDO|idx|a:b=13,hi', do._key())
        pipe.sadd('TestDO|idx|a:b', 'TestDO|idx|a:b=13,hi')
        pipe.execute().AndReturn([])
        self.mox.ReplayAll()

        do.update(lock=lock)

    def test_delete_redis(self):
        conn = self.mox.CreateMockAnything()
        do = TestDO(conn)
        do.k = 3
        do.v = 7
        # Converting this into a sorted OrderedDict so that the calls below are in the right order
        do._index_map = collections.OrderedDict(sorted(do._index_map.items()))
        lock = self.context()
        pipe = self.mox.CreateMockAnything()
        conn.pipeline().AndReturn(self.context(pipe))
        pipe.delete(do._key())
        pipe.srem(do._table_records_key, do._key())
        pipe.srem('TestDO|idx|a=None', do._key())
        pipe.srem('TestDO|idx|a:b=None,None', do._key())
        pipe.execute().AndReturn([])
        self.mox.ReplayAll()

        do.delete(lock=lock)

    def test_get_partial_key(self):
        with self.assertRaises(orm.UnrecoverableORMException):
            TestDO.get(None, k=1)

    def test_get_bad_key(self):
        with self.assertRaises(orm.UnrecoverableORMException):
            TestDO.get(None, k=1, a=2)

    def test_get_empty(self):
        conn = self.mox.CreateMockAnything()
        conn.hgetall('TestDO|rec|k=1:v=2').AndReturn({})
        self.mox.ReplayAll()
        TestDO.get(conn, k=1, v=2)

    def test_get(self):
        conn = self.mox.CreateMockAnything()
        conn.hgetall('TestDO|rec|k=1:v=2').AndReturn({'a': 1})
        self.mox.ReplayAll()
        TestDO.get(conn, k=1, v=2)

    def test_get_self(self):
        self.mox.StubOutWithMock(TestDO, 'get')
        TestDO.get(None, k=1, v=2)
        self.mox.ReplayAll()
        do = TestDO(None)
        do.k = 1
        do.v = 2
        do.get_self()

    def test_get_by_index_empty_clauses(self):
        with self.assertRaises(orm.UnrecoverableORMException):
            TestDO.get_by_index(None)

    def test_get_by_index_undefined_index(self):
        with self.assertRaises(orm.UnrecoverableORMException):
            TestDO.get_by_index(None, undefined=None, undefined2=42)

    def test_get_by_index_primary_key_no_record(self):
        self.mox.StubOutWithMock(TestDO, 'get')
        TestDO.get(None, k=1, v=2).AndReturn(None)
        self.mox.ReplayAll()
        self.assertEqual(TestDO.get_by_index(None, k=1, v=2), [])

    def test_get_by_index_primary_key(self):
        self.mox.StubOutWithMock(TestDO, 'get')
        rec = self.mox.CreateMockAnything()
        TestDO.get(None, k=1, v=2).AndReturn(rec)
        self.mox.ReplayAll()
        self.assertEqual(TestDO.get_by_index(None, k=1, v=2), [rec])

    def test_get_by_index_no_records(self):
        conn = self.mox.CreateMockAnything()
        conn.smembers(TestDO._index_key_values(TestDO._index_name(['a']), {'a': 1})).AndReturn([])
        self.mox.ReplayAll()
        self.assertEqual(TestDO.get_by_index(conn, a=1), [])

    def test_get_by_index_missing_record(self):
        conn = self.mox.CreateMockAnything()
        conn.smembers(TestDO._index_key_values(TestDO._index_name(['a']), {'a': 1})).AndReturn(['r1', 'r2'])
        conn.hgetall('r1').AndReturn(None)
        conn.hgetall('r2').AndReturn({'a': 1})
        self.mox.ReplayAll()
        self.assertEqual(TestDO.get_by_index(conn, a=1), [TestDO.from_dict(conn, {'a': 1})])

    def test_get_by_index(self):
        conn = self.mox.CreateMockAnything()
        conn.smembers(TestDO._index_key_values(TestDO._index_name(['a']), {'a': 1})).AndReturn(['r1', 'r2'])
        conn.hgetall('r1').AndReturn({'b': 2})
        conn.hgetall('r2').AndReturn({'a': 1})
        self.mox.ReplayAll()
        self.assertEqual(
            TestDO.get_by_index(conn, a=1),
            [TestDO.from_dict(conn, {'b': 2}), TestDO.from_dict(conn, {'a': 1})])

    def test_get_columns_all(self):
        conn = self.mox.CreateMockAnything()
        pipe = self.mox.CreateMockAnything()
        conn.pipeline().AndReturn(self.context(pipe))
        conn.smembers(TestDO._table_records_key).AndReturn([1, 2, 3])
        pipe.hmget(1, TestDO._cols())
        pipe.hmget(2, TestDO._cols())
        pipe.hmget(3, TestDO._cols())
        pipe.execute().AndReturn([3, 2, 1])
        self.mox.ReplayAll()
        self.assertEqual(TestDO.get_columns(conn), [3, 2, 1])

    def test_get_columns(self):
        conn = self.mox.CreateMockAnything()
        pipe = self.mox.CreateMockAnything()
        conn.pipeline().AndReturn(self.context(pipe))
        conn.smembers(TestDO._table_records_key).AndReturn([1, 2, 3])
        pipe.hmget(1, ['a', 'b'])
        pipe.hmget(2, ['a', 'b'])
        pipe.hmget(3, ['a', 'b'])
        pipe.execute().AndReturn([3, 2, 1])
        self.mox.ReplayAll()
        self.assertEqual(TestDO.get_columns(conn, ['a', 'b']), [3, 2, 1])

    def test_init(self):
        # for coverage only
        orm.Worker(None)
        orm.Migration(None)
        orm.Table(None)
        orm.Chunk(None)


class TestORMMigration(mox.MoxTestBase):
    def test_get_latest(self):
        self.mox.StubOutWithMock(orm.Migration, 'get_by_index')
        migrations = []
        for i in [5, 3, 7, 2, 4]:
            migrations.append(orm.Migration.from_dict(None, {'start_time': i}))
        orm.Migration.get_by_index(None, a=1, b=2).AndReturn(migrations)
        self.mox.ReplayAll()
        self.assertEqual(orm.Migration.get_latest(None, a=1, b=2).start_time, 7)

    def test_get_latest_None(self):
        self.mox.StubOutWithMock(orm.Migration, 'get_by_index')
        migrations = []
        orm.Migration.get_by_index(None, a=1, b=2).AndReturn(migrations)
        self.mox.ReplayAll()
        self.assertEqual(orm.Migration.get_latest(None, a=1, b=2), None)
