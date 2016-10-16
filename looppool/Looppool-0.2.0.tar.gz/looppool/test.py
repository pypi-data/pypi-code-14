import os
import logging
import functools
import traceback
import collections
from multiprocessing import Queue
from unittest import mock
from pprint import pformat

from tornado import testing, gen

from . import Pool, Worker, SafeWorker, task_done
from .utility import ResourceReporter


def setUpModule():
    if os.environ.get('DUMMY_MULTIPROCESSING_TEST'):
        import multiprocessing.dummy as mp
        import looppool
        looppool.mp = mp


class CalcWorker(Worker):
    
    @gen.coroutine
    def _process_message(self, message):
        yield gen.sleep(0.01)
        self._result_queue.put_nowait(message * 2)


class SafeCalcWorker(SafeWorker):
    
    @gen.coroutine
    def _process_message(self, message):
        try:
            yield gen.sleep(0.01)
            self._result_queue.put_nowait(message * 2)
        finally:
            self._task_queue.task_done()


class NumWorker(Worker):
    
    def _process_message(self, message):
        self._result_queue.put_nowait(self._number)


class SafeNumWorker(SafeWorker):
    
    @task_done
    def _process_message(self, message):
        self._result_queue.put_nowait(self._number)
  
        
class StatefulWorker(Worker):
    
    state = 0


    def get(self):
        return self.state

    def set(self, state):
        self.state = state
    
    def power(self, p):
        return self.state ** p
    
    def _process_message(self, message):
        cmd, *args = message
        self._result_queue.put_nowait((cmd, getattr(self, cmd)(*args), self._number))

        
class SafeStatefulWorker(SafeWorker, StatefulWorker):
    
    @task_done
    @gen.coroutine
    def _process_message(self, message):
        cmd, *args = message
        self._result_queue.put_nowait((cmd, getattr(self, cmd)(*args), self._number))


class RaisingWorker(Worker):
        
    _log_buffer = None

    
    def _initialise(self):
        self._log_buffer = logging.handlers.BufferingHandler(1024)
        
        tornado_app_logger = logging.getLogger('tornado.application') 
        tornado_app_logger.handlers.clear()
        tornado_app_logger.propagate = False
        tornado_app_logger.addHandler(self._log_buffer)
    
    def raise_error(self):
        raise RuntimeError('Worker has broken')
        
    def get_log(self):
        return [(entry.getMessage(), traceback.format_exception(*entry.exc_info)) 
            for entry in self._log_buffer.buffer]
    
    def _process_message(self, cmd):
        self._result_queue.put_nowait((cmd, getattr(self, cmd)()))
        

class SafeRaisingWorker(SafeWorker, RaisingWorker):
    
    @task_done
    def _process_message(self, cmd):
        self._result_queue.put_nowait((cmd, getattr(self, cmd)()))
  

class TestCase(testing.AsyncTestCase):
    
    result_list = None
    
    testee = None
    
    
    def setUp(self):
        super().setUp()

        self.testee = self.get_testee()
        self.result_list = []
    
    def process_message(self, message):
        self.result_list.append(message)
        
    def get_testee(self):
        raise NotImplementedError
        

class TestPoolCalcWorker(TestCase):
    
    def get_testee(self):
        pool = Pool(self.io_loop, pool_size=8, worker_class=CalcWorker)
        pool.process_message = self.process_message
        
        return pool 
    
    @testing.gen_test
    def test_basic(self):
        self.testee.start()
        list(map(self.testee.put_nowait, range(10)))
        
        # Task are on worker's loops, wait for them
        yield gen.sleep(0.05)
            
        self.testee.stop()

        self.assertEqual({2, 0, 6, 4, 8, 10, 12, 14, 16, 18}, set(self.result_list))
        
    @testing.gen_test
    def test_worker_shutdown(self):
        # Some of threads pass barrier with poison pills
        for i in range(16):
            pool = self.get_testee()
            
            pool.start()
            list(map(pool.put_nowait, range(i)))
            pool.stop()


class TestPoolSafeCalcWorker(TestPoolCalcWorker):
    
    def get_testee(self):
        pool = Pool(self.io_loop, pool_size=8, worker_class=SafeCalcWorker)
        pool.process_message = self.process_message
        
        return pool
    
    @testing.gen_test
    def test_basic(self):
        self.testee.start()
        list(map(self.testee.put_nowait, range(10)))
        self.testee.stop()
        
        # Task results are on the loop in scheduled callbacks, so get after them
        yield gen.Task(self.io_loop.add_callback)

        self.assertEqual({2, 0, 6, 4, 8, 10, 12, 14, 16, 18}, set(self.result_list))
        
    @testing.gen_test
    def test_basic_callback(self):
        self.testee.start()
        list(map(self.testee.put_nowait, range(10)))
        self.testee.stop()
        
        # Task results are on the loop in scheduled callbacks, so get after them
        def check():
            self.assertEqual({2, 0, 6, 4, 8, 10, 12, 14, 16, 18}, set(self.result_list))
        self.io_loop.add_callback(check)
    
    def test_invalid_task_queue(self):
        queue = Queue()
        with self.assertRaises(AssertionError) as ctx:
            Pool(self.io_loop, pool_size=2, worker_class=SafeCalcWorker, task_queue=queue)
        self.assertEqual('Task queue must be a joinable queue', str(ctx.exception))


class TestPoolNumWorker(TestCase):
    
    def get_testee(self):
        pool = Pool(self.io_loop, pool_size=8, worker_class=NumWorker)
        pool.process_message = self.process_message
        
        return pool
    
    @testing.gen_test
    def test_worker_task_distribution(self):
        self.testee.start()
        list(map(self.testee.put_nowait, range(800)))
        self.testee.stop()

        # Task results are on the loop in scheduled callbacks, so get after them
        yield gen.Task(self.io_loop.add_callback)

        occurrence = {i : self.result_list.count(i) for i in range(8)}
        self.assertEqual({i : 100 for i in range(8)}, occurrence)

  
class TestPoolSafeNumWorker(TestPoolNumWorker):
    
    def get_testee(self):
        pool = Pool(self.io_loop, pool_size=8, worker_class=SafeNumWorker)
        pool.process_message = self.process_message
        
        return pool


class TestPoolStatefulWorker(TestCase):
    
    def get_testee(self):
        pool = Pool(self.io_loop, pool_size=8, worker_class=StatefulWorker)
        pool.process_message = self.process_message
        
        return pool
    
    @testing.gen_test
    def test_worker_barrrier_align(self):
        for init_msg_num in range(16):
            self.result_list.clear()
            pool = self.get_testee()
            
            pool.start()
            
            for i in range(init_msg_num):
                pool.put_nowait(('power', i))

            for _ in range(2 * pool.pool_size - 1):
                pool.put_nowait(('set', 26))
                  
            for _ in range(2 * pool.pool_size - 1):
                pool.put_nowait(('get',))
            
            pool.stop()
            
            # Task results are on the loop in scheduled callbacks, so get after them
            yield gen.Task(self.io_loop.add_callback)
            
            def reducer(r, v):
                r[v[2]].append(v)
                return r
            
            def get_per_worker_results(l):
                return functools.reduce(reducer, l, collections.defaultdict(list))
            
            self.assertTrue(all(r[1] == 26 for r in self.result_list if r[0] == 'get'),
                'Init messages {}:\n {}'.format(init_msg_num, 
                    pformat(get_per_worker_results(self.result_list))))


class TestPoolSafeStatefulWorker(TestPoolStatefulWorker):
    
    def get_testee(self):
        pool = Pool(self.io_loop, pool_size=8, worker_class=SafeStatefulWorker)
        pool.process_message = self.process_message
        
        return pool


class TestPoolRaisingWorker(TestCase):
    
    def get_testee(self):
        pool = Pool(self.io_loop, pool_size=8, worker_class=RaisingWorker)
        pool.process_message = self.process_message
        
        return pool
    
    @testing.gen_test
    def test_error(self):
        # Make sure workers are operable after raised exception
                
        self.testee.start()
        
        for _ in range(self.testee.pool_size):
            self.testee.put_nowait('raise_error')

        for _ in range(self.testee.pool_size):
            self.testee.put_nowait('get_log')
        
        self.testee.stop()
        
        # Task results are on the loop in scheduled callbacks, so get after them
        yield gen.Task(self.io_loop.add_callback)
        
        self.assertEqual(self.testee.pool_size, len(self.result_list))
        for _, result in self.result_list:
            for msg, tb in result:
                self.assertTrue(msg.startswith('Exception in callback'))
                self.assertTrue(tb[-1].strip().endswith('RuntimeError: Worker has broken'))


class TestPoolSafeRaisingWorker(TestPoolRaisingWorker):
    
    def get_testee(self):
        pool = Pool(self.io_loop, pool_size=8, worker_class=SafeRaisingWorker)
        pool.process_message = self.process_message
        
        return pool


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
        self.assertTrue(0 <= actual[7][1][1] < 1, 'Actual usage is {}'.format(actual[7][1][1]))
        
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

