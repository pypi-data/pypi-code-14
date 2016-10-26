'''
Process pool running Tornado IO loops and communicates with parent process via
message queues.  
'''


import signal
import threading
import multiprocessing as mp

from tornado import ioloop, gen


__all__ = 'Pool', 'Worker', 'task_done'


def _create_worker(worker_class, number, task_queue, result_queue):
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
 
    worker = worker_class(number, loop, task_queue, result_queue)
    worker.start()
    
    # Stopped by manager._task_queue_listener on receiving a poison pill
    loop.start()
    loop.close()
    worker.join()


def task_done(fn):
    '''Decorator to call ``self._task_done()`` on return of 
    ``Worker._process_message`` and ``result_done()`` on 
    return of Pool.process_message'''
    
    @gen.coroutine
    def task_done_wrapper(*args):
        try:
            result = fn(*args)
            if gen.is_future(result):
                return (yield result)
            else:
                return result
        finally:
            if isinstance(args[0], Worker):
                args[0]._task_done()
            else:
                args[-1]()
    
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
    '''Output queue. It doesn't necessary mean that input messages are 1-to-1
    to output messages.'''

    _task_queue_listener = None
    '''Thread that listens to task queue'''
    
    _number = None
    '''Process number'''
    
    _running_tasks = None
    '''Thread semaphore to limit number of running tasks'''
    
    
    def __init__(self, number, ioloop, task_queue, result_queue):
        self._number = number
        self._ioloop = ioloop
        self._task_queue = task_queue
        self._result_queue = result_queue
        
        effective_max_size = task_queue._maxsize \
            if hasattr(task_queue, '_maxsize') else task_queue.maxsize
        self._running_tasks = threading.Semaphore(effective_max_size)
        self._task_queue_listener = threading.Thread(target=self._task_queue_listener_worker)
        
        self._initialise()
    
    def _initialise(self):
        '''Just an initialising method to override without need to call parent method'''
    
    def _task_queue_listener_worker(self):
        '''Thread target to listen task queue.'''
        
        for message in iter(self._get_task, PoisonPill):
            self._ioloop.add_callback(self._process_message, message)
        else:
            # Mark poison pill as done
            self._task_queue.task_done()
            self._task_queue.join() 
            
            # Let remaining task callbacks complete
            self._ioloop.add_callback(self._ioloop.stop)
  
    def _get_task(self):
        self._running_tasks.acquire()
        return self._task_queue.get()
  
    def _task_done(self):
        self._task_queue.task_done()
        self._running_tasks.release()
  
    def _put_nowait(self, result):
        self._result_queue.put_nowait(result)
  
    @gen.coroutine
    def _process_message(self, task):
        '''Must be overridden in subclass, like::
            
            try:
                result = 'some processing'
                self._put_nowait(result)
            finally:
                self._task_done()
        '''
        raise NotImplementedError
    
    def start(self):
        self._task_queue_listener.start()
        
    def join(self):
        self._task_queue_listener.join()


class Pool:
    '''IO loop pool'''

    pool_size = None
    '''Number of processes in pool'''
    
    _ioloop = None
    '''Main process's Tornado IO loop'''
    
    _task_queue_list = None
    '''Input queue list, queue per worker'''
    
    _result_queue = None
    '''Output queue. It doesn't necessary mean that input message are 1-to-1
    to output messages.'''
    
    _pool = None
    '''List of ``multiprocessing.Process`` objects'''
    
    _result_queue_listener = None
    '''Thread that listens to result queue'''
    
    _sequence_number = 0
    '''`Number incremented on every message put into task queue for distribute
    tasks between workers.'''
    
    _pending_results = None
    '''Thread semaphore to limit number of pending results'''
    
    _running = None
    '''Pool run flag '''
    
    
    def __init__(self, ioloop, pool_size, worker_class = Worker, target = _create_worker,
        max_tasks = 4096, max_results = 4096):
        
        self.pool_size = pool_size
        self._ioloop = ioloop
        
        self._task_queue_list = [mp.JoinableQueue(max_tasks // pool_size) 
            for _ in range(pool_size)]
        self._result_queue = mp.JoinableQueue(max_results)
        
        self._pool = [mp.Process(target = target,
            args = (worker_class, i, task_queue, self._result_queue))
            for i, task_queue in enumerate(self._task_queue_list)]
        
        effective_max_size = self._result_queue._maxsize \
            if hasattr(self._result_queue, '_maxsize') else self._result_queue.maxsize
        self._pending_results = threading.Semaphore(effective_max_size)
        self._result_queue_listener = threading.Thread(target = self._result_queue_listener_worker)
    
    def _result_queue_listener_worker(self):
        '''Thread target to listen result queue'''
        
        for message in iter(self._get_result, PoisonPill):
            self._ioloop.add_callback(self.process_message, message, self._result_done)
    
    def _get_result(self):
        # The loop is to allow skip the limit on ``stop()`` when result queue was full
        while self._running and not self._pending_results.acquire(timeout = 0.1):
            pass
        else:
            return self._result_queue.get()
    
    def _result_done(self):
        self._result_queue.task_done()
        self._pending_results.release()
    
    def start(self):
        list(map(mp.Process.start, self._pool))
        self._result_queue_listener.start()
        
        self._running = True
    
    def stop(self):
        '''Poison pill sender'''
        
        self._running = False
        
        for q in self._task_queue_list:
            q.put(PoisonPill)
        else:
            list(map(mp.Process.join, self._pool))
        
        self._result_queue.put(PoisonPill)
        self._result_queue_listener.join()
        
    def put_nowait(self, message, worker_num = None):
        '''Puts a task message into the queue. If *worker_num* argument is given
        it must be a number of worker which should receive the the message. Otherwise
        round-robin is used.'''

        if worker_num is not None:
            task_queue = self._task_queue_list[worker_num]
        else:
            task_queue = self._task_queue_list[self._sequence_number % self.pool_size]
            self._sequence_number += 1
        
        task_queue.put_nowait(message)

    @staticmethod
    @gen.coroutine
    def process_message(result, result_done):
        '''Re-assign or override. Must call ``result_done()``'''
        
        raise NotImplementedError

