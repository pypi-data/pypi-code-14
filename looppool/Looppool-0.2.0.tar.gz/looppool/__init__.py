'''
Process pool running Torando IO loops and communicates with parent process via
message queues.  
'''


import signal
import threading
import multiprocessing as mp

from tornado import ioloop, gen


__all__ = 'Pool', 'Worker', 'SafeWorker', 'task_done'


def _create_worker(worker_class, number, task_queue, result_queue, barrier):
    '''This function is executed in a separate process'''
    
    # Child processes receive the same signal the parent receives
    # but because the workers are stopped via sending poison pills
    # the signals are destructive. 
    # Check for main thread is for coverage testing with ``multiprocessing.dummy``.
    if threading.current_thread() == threading.main_thread():
        signal.signal(signal.SIGINT, signal.SIG_IGN)
        signal.signal(signal.SIGTERM, signal.SIG_IGN)
    
    loop = ioloop.IOLoop()
    loop.make_current()
 
    worker = worker_class(number, loop, task_queue, result_queue, barrier)
    worker.start()
    
    # Stopped by manager._task_queue_listener on receiving a poison pill
    loop.start()
    loop.close()
    worker.join()


def task_done(fn):
    '''Decorator to calls ``self._task_queue.task_done()`` on return of 
    ``SafeWorker._process_message``'''
    
    @gen.coroutine
    def task_done_wrapper(self, message):
        assert isinstance(self, SafeWorker), '@task_done must be applied only on SafeWorker'
        try:
            result = fn(self, message)
            if gen.is_future(result):
                return (yield result)
            else:
                return result
        finally:
            self._task_queue.task_done()
    
    return task_done_wrapper


class PoisonPill:
    '''A little better than just ``None``'''


class Worker:
    '''Worker process'''

    _ioloop = None
    '''Process's Tornado IO loop'''
    
    _task_queue = None
    '''Input queue'''
    
    _result_queue = None
    '''Output queue. It doesn't necessary mean that input message are 1-to-1
    to output messages.'''

    _barrier = None
    '''Barrier to guarantee even distribution of tasks. Note that tasks
    are read from queue in a thread to work's IO loop and involve to delay
    on the thread otherwise.'''

    _task_queue_listener = None
    '''Thread that listens to task queue'''
    
    _number = None
    '''Process number'''
    
    
    def __init__(self, number, ioloop, task_queue, result_queue, barrier):
        self._number = number
        self._ioloop = ioloop
        self._task_queue = task_queue
        self._result_queue = result_queue
        self._barrier = barrier
        
        self._task_queue_listener = threading.Thread(target=self._task_queue_listener_worker)
        
        self._initialise()
    
    def _initialise(self):
        '''Just an initialising method to override to without need to call parent method'''
    
    def _task_queue_listener_worker(self):
        '''Thread target to listen task queue.'''
        
        for message in iter(self._task_queue.get, PoisonPill):
            self._ioloop.add_callback(self._process_message, message)
            try:
                self._barrier.wait()
            except threading.BrokenBarrierError:
                pass
        else:
            self._barrier.abort()
                
        self._on_task_queue_listener_worker_stop()
                
    def _on_task_queue_listener_worker_stop(self):
        self._ioloop.add_callback(self._ioloop.stop)

    @gen.coroutine
    def _process_message(self, message):
        '''Must be overridden in subclass, like::
        
            result = 'some processing'
            self._result_queue.put_nowait(result)
        '''
        raise NotImplementedError

    def start(self):
        self._task_queue_listener.start()
        
    def join(self):
        self._task_queue_listener.join()


class SafeWorker(Worker):
    '''Worker that waits until its tasks on IO loop are done on stop'''
  
    def _on_task_queue_listener_worker_stop(self):
        self._task_queue.task_done() # mark poison pill is done
        self._task_queue.join()
        
        super()._on_task_queue_listener_worker_stop()
    
    @gen.coroutine
    def _process_message(self, message):
        '''Must be overridden in subclass, like::
            
            try:
                result = 'some processing'
                self._result_queue.put_nowait(result)
            finally:
                self._task_queue.task_done()
        '''
        raise NotImplementedError


class Pool:
    '''IO loop pool'''

    pool_size = None
    '''Number of processes in pool'''
    
    _ioloop = None
    '''Main process's Tornado IO loop'''
    
    _task_queue = None
    '''Input queue'''
    
    _result_queue = None
    '''Output queue. It doesn't necessary mean that input message are 1-to-1
    to output messages.'''
    
    _pool = None
    '''List of ``multiprocessing.Process`` objects'''
    
    _result_queue_listener = None
    '''Thread that listens to result queue'''
    
    _barrier = None
    '''Barrier to guarantee even distribution of tasks. Note that tasks
    are read from queue in a thread to work's IO loop and involve to delay
    on the thread otherwise.'''
    
    
    def __init__(self, ioloop, pool_size, worker_class = Worker, target = _create_worker,
        task_queue = None, result_queue = None):
        
        self.pool_size = pool_size
        self._ioloop = ioloop
        
        if issubclass(worker_class, SafeWorker):
            jq = mp.JoinableQueue()
            self._task_queue = task_queue or jq
            # mp.JoinableQueue is multiprocessing context's method
            assert isinstance(self._task_queue, type(jq)), 'Task queue must be a joinable queue'
        else:
            self._task_queue = task_queue or mp.Queue()
        
        self._result_queue = result_queue or mp.Queue()
        
        self._barrier = mp.Barrier(pool_size)
        
        self._pool = [mp.Process(target=target,
            args=(worker_class, i, self._task_queue, self._result_queue, self._barrier))
            for i in range(pool_size)]
        
        self._result_queue_listener = threading.Thread(target=self._result_queue_listener_worker)
    
    def _result_queue_listener_worker(self):
        '''Thread target to listen task queue'''
        
        for message in iter(self._result_queue.get, PoisonPill):
            self._ioloop.add_callback(self.process_message, message)
    
    def start(self):
        list(map(mp.Process.start, self._pool))
        self._result_queue_listener.start()
    
    def stop(self):
        '''Poison pill sender'''
        
        for _ in self._pool:
            self._task_queue.put_nowait(PoisonPill)
        else:
            list(map(mp.Process.join, self._pool))
        
        self._result_queue.put_nowait(PoisonPill)
        self._result_queue_listener.join()
        
    def put_nowait(self, message):
        self._task_queue.put_nowait(message)
    
    @staticmethod
    @gen.coroutine
    def process_message(message):
        '''Re-assign or override'''
        
        raise NotImplementedError

