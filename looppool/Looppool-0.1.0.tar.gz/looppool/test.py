import os
from multiprocessing import Queue
from unittest import mock

from tornado import testing, gen

from . import Pool, Worker, SafeWorker
from .utility import ResourceReporter


def setUpModule():
    if os.environ.get('DUMMY_MULTIPROCESSING_TEST'):
        import multiprocessing.dummy as mp
        import looppool
        looppool.mp = mp


class Mul2Worker(Worker):
    
    @gen.coroutine
    def _process_message(self, message):
        yield gen.sleep(0.01)
        self._result_queue.put_nowait(message * 2)


class SafeMul2Worker(SafeWorker):
    
    @gen.coroutine
    def _process_message(self, message):
        yield gen.sleep(0.01)
        
        self._result_queue.put_nowait(message * 2)
        self._task_queue.task_done()


class NumWorker(Worker):
    
    @gen.coroutine
    def _process_message(self, message):
        self._result_queue.put_nowait(self._number)


class SafeNumWorker(SafeWorker):
    
    @gen.coroutine
    def _process_message(self, message):
        self._result_queue.put_nowait(self._number)
        self._task_queue.task_done()


class TestPool(testing.AsyncTestCase):
    
    result_list = None
    
    
    def setUp(self):
        super().setUp()

        self.result_list = []
    
    def process_message(self, message):
        self.result_list.append(message)
    
    @testing.gen_test
    def test_basic(self):
        pool = Pool(self.io_loop, pool_size=2, worker_class=Mul2Worker)
        pool.process_message = self.process_message
        
        pool.start()
        list(map(pool.put_nowait, range(10)))
        
        # Task are on worker's loops, wait for them
        yield gen.sleep(0.05)
            
        pool.stop()

        self.assertEqual({2, 0, 6, 4, 8, 10, 12, 14, 16, 18}, set(self.result_list))

    @testing.gen_test
    def test_worker_distribution(self):
        pool = Pool(self.io_loop, pool_size=8, worker_class=NumWorker)
        pool.process_message = self.process_message
        
        pool.start()
        list(map(pool.put_nowait, range(800)))
        pool.stop()

        # Task results are on the loop in scheduled callbacks, so get after them
        def check():
            occurrence = {i : self.result_list.count(i) for i in range(8)}
            self.assertEqual({i : 100 for i in range(8)}, occurrence)
        self.io_loop.add_callback(check)
        
    @testing.gen_test
    def test_worker_shutdown(self):
        # Some of threads pass barrier with poison pills
        for i in range(16):
            pool = Pool(self.io_loop, pool_size=8, worker_class=Mul2Worker)
            pool.process_message = self.process_message
            
            pool.start()
            list(map(pool.put_nowait, range(i)))
            pool.stop()


class TestSafePool(testing.AsyncTestCase):
    
    result_list = None
    
    
    def setUp(self):
        super().setUp()

        self.result_list = []
    
    def process_message(self, message):
        self.result_list.append(message)
    
    def test_invalid_task_queue(self):
        queue = Queue()
        with self.assertRaises(AssertionError) as ctx:
            Pool(self.io_loop, pool_size=2, worker_class=SafeMul2Worker, task_queue=queue)
        self.assertEqual('Task queue must implement join()', str(ctx.exception))
    
    @testing.gen_test
    def test_basic(self):
        pool = Pool(self.io_loop, pool_size=2, worker_class=SafeMul2Worker)
        pool.process_message = self.process_message
        
        pool.start()
        list(map(pool.put_nowait, range(10)))
        pool.stop()
        
        # Task results are on the loop in scheduled callbacks, so get after them
        def check():
            self.assertEqual({2, 0, 6, 4, 8, 10, 12, 14, 16, 18}, set(self.result_list))
        self.io_loop.add_callback(check)

    @testing.gen_test
    def test_basic_task_wait(self):
        pool = Pool(self.io_loop, pool_size=2, worker_class=SafeMul2Worker)
        pool.process_message = self.process_message
        
        pool.start()
        list(map(pool.put_nowait, range(10)))
        pool.stop()
        
        # Task results are on the loop in scheduled callbacks, so get after them
        yield gen.Task(self.io_loop.add_callback)

        self.assertEqual({2, 0, 6, 4, 8, 10, 12, 14, 16, 18}, set(self.result_list))
        
    @testing.gen_test
    def test_worker_distribution(self):
        pool = Pool(self.io_loop, pool_size=8, worker_class=SafeNumWorker)
        pool.process_message = self.process_message
        
        pool.start()
        list(map(pool.put_nowait, range(800)))
        pool.stop()

        # Task results are on the loop in scheduled callbacks, so get after them
        def check():
            occurrence = {i : self.result_list.count(i) for i in range(8)}
            self.assertEqual({i : 100 for i in range(8)}, occurrence)
        self.io_loop.add_callback(check)
        
    @testing.gen_test
    def test_worker_shutdown(self):
        # Some of threads pass barrier with poison pills
        for i in range(16):
            pool = Pool(self.io_loop, pool_size=8, worker_class=SafeNumWorker)
            pool.process_message = self.process_message
            
            pool.start()
            list(map(pool.put_nowait, range(i)))
            pool.stop()


class TestResourceReporter(testing.AsyncTestCase):
    
    @testing.gen_test
    def test(self):
        statsd = mock.MagicMock()
       
        testee = ResourceReporter(self.io_loop, statsd, prefix='pool.worker.1')
        testee.sleep_time = 0.1
        
        testee.start()
        yield gen.sleep(0.2)
        testee.stop()

        self.assertEqual([(), ()], statsd.pipeline.call_args_list)
        
        actual = statsd.pipeline().mock_calls
        
        self.assertTrue(isinstance(actual[1][1][1], int))
        self.assertGreater(actual[1][1][1], 10 * 1024)
        self.assertTrue(0.9 < actual[1][1][1] / actual[8][1][1] < 1.1)
        
        self.assertTrue(isinstance(actual[7][1][1], float))
        self.assertTrue(0 < actual[7][1][1] < 1)
        
        self.assertEqual([
            mock.call.__enter__(),
            mock.call.__enter__().gauge('pool.worker.1.rss', actual[1][1][1]),
            mock.call.__enter__().gauge('pool.worker.1.ioloop.handler', 1),
            mock.call.__enter__().gauge('pool.worker.1.ioloop.callback', 0),
            mock.call.__enter__().gauge('pool.worker.1.ioloop.timeout', 2),
            mock.call.__exit__(None, None, None),
            mock.call.__enter__(),
            mock.call.__enter__().gauge('pool.worker.1.cpu', actual[7][1][1]),
            mock.call.__enter__().gauge('pool.worker.1.rss', actual[8][1][1]),
            mock.call.__enter__().gauge('pool.worker.1.ioloop.handler', 1),
            mock.call.__enter__().gauge('pool.worker.1.ioloop.callback', 0),
            mock.call.__enter__().gauge('pool.worker.1.ioloop.timeout', 2),
            mock.call.__exit__(None, None, None)
        ], actual)

