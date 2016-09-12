from __future__ import absolute_import
import functools
from threading import RLock, Thread


def synchronized(wrapped):
    """
    A simple decorator to synchronize an instance method. The RLock object
    is saved into the wrapped function itself
    """
    _LOCK_NAME = "_synchronized_lock"

    lock = vars(wrapped).get(_LOCK_NAME, None)
    if not lock:
        lock = vars(wrapped).setdefault(_LOCK_NAME, RLock())
        
    @functools.wraps(wrapped)
    def _wrapper(*args, **kwargs):
        with lock:
            return wrapped(*args, **kwargs)
    return _wrapper


def run_async(wrapped):
    """
        run_async(wrapped)
            function decorator, intended to make "func" run in a separate
            thread (asynchronously).
            Returns the created Thread object

            E.g.:
            @run_async
            def task1():
                do_something

            @run_async
            def task2():
                do_something_too

            t1 = task1()
            t2 = task2()
            ...
            t1.join()
            t2.join()
    """

    @functools.wraps(wrapped)
    def async_func(*args, **kwargs):
        func_hl = Thread(target=wrapped, args=args, kwargs=kwargs)
        func_hl.start()
        return func_hl

    return async_func


if __name__ == "__main__":
    from time import sleep

    @run_async
    def print_somedata():
        print('starting print_somedata')
        sleep(2)
        print('print_somedata: 2 sec passed')
        sleep(2)
        print('print_somedata: 2 sec passed')
        sleep(2)
        print('finished print_somedata')


    def main():
        print_somedata()
        print('back in main')
        print_somedata()
        print('back in main')
        print_somedata()
        print('back in main')

    main()
