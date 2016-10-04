from multiprocessing import TimeoutError
from multiprocessing.pool import ThreadPool as Pool

pool = Pool()

def timeout(seconds, f, args=(), kwargs={}, silent=False):
    try:
        return pool.apply_async(f, args, kwargs).get(seconds)
    except TimeoutError:
        if silent:
            return
        else:
            raise
