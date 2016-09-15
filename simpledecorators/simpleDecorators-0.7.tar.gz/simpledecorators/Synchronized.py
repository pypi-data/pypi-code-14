from threading import RLock

import traceback

def Synchronized(lock=None):
    """

    :param lock: if None - global lock will used, unique for each function
    :return:
    """
    if not lock:
        lock=RLock()
    def decorator(fn):
        def wrapped(*args, **kwargs):
            lock.acquire()
            try:
                return fn(*args, **kwargs)
            finally:
                lock.release()

        wrapped.__name__ = fn.__name__ + "Synchronized_wrapped"
        return wrapped

    return decorator
