# coding=utf-8
"""
Description
===========

This is a small utility module where utility classes and functions can be
stored and exported.

"""

__author__ = 'Scott Schaefer'

from threading import Thread
import queue

class ThreadPool:
    def __init__(self, num_workers):
        self._max_threads = num_workers
        self.tasks = queue.Queue()
        for _ in range(num_workers):
            t = Thread(target=self.worker, daemon=True)
            t.start()

    def add(self, target, *args, **kwargs):
        self.tasks.put((target, args, kwargs))

    def join(self):
        self.tasks.join()

    def worker(self):
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
