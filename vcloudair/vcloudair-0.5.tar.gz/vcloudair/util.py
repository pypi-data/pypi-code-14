# coding=utf-8
"""
Utility Module
==============

This is a small utility module where utility classes and functions can be
stored and exported.

"""

__author__ = 'Scott Schaefer'

from threading import Thread
import queue

UUID_L = 36

class ThreadPool:
    """
    :param int num_workers: The number of threads that exist in the pool

    A basic thread pooling class to allow a set number of threads to pick up
    work items submitted to a queue. Threads are started as soon as the class
    is instantiated. They run in daemon mode and so will end if the main thread
    ends.
    """

    def __init__(self, num_workers):
        self._max_threads = num_workers
        self.tasks = queue.Queue()
        for _ in range(num_workers):
            t = Thread(target=self._worker, daemon=True)
            t.start()

    def add(self, target, *args, **kwargs):
        """
        Adds a call to the thread pool along with the associated arguments
        and/or keyword arguments.

        :param func target: The target callable object for the thread,
         usually a function.
        :param args: The arguments to pass into the callable
        :param kwargs: The keyword arguments to pass into the callable
        :return: ``None``
        """
        self.tasks.put((target, args, kwargs))

    def join(self):
        """
        Join against the internal queue datastructure until it's empty. This is
        a blocking call which will force the program to wait until the queue is
        empty to continue with execution.

        :return: ``None``
        """
        self.tasks.join()

    def _worker(self):
        while True:
            target,args,kwargs = self.tasks.get()
            try:
                target(*args, **kwargs)
            except Exception:
                pass
            finally:
                self.tasks.task_done()

def check_http_response_error(response):
    """
    Verify that the HTTP request did not return an error.
    If error is returned, raise a runtime exception with the status and
    reason.

    :param response: Requests response object
    :return: None
    :raises: RuntimeError
    """
    if response.status_code >= 400:
        errormsg = '{}, {}\n{}'.format(response.status_code,
                                       response.reason,
                                       response.text)
        raise RuntimeError(errormsg)
