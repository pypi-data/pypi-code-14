import time

import redlock
from retrying import retry


class Error(Exception):
    pass


class ReentrantRedLock(redlock.ReentrantRedLock):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('retry_times', 1)
        kwargs.setdefault('retry_delay', 50)
        super(ReentrantRedLock, self).__init__(*args, **kwargs)

    @retry(
        wait_exponential_multiplier=50, wait_exponential_max=500,
        # introduce up to 200ms randomly on each wait time
        wait_jitter_max=200,
        # wait up to a total of 20s
        stop_max_delay=20000,
        # retry if the result is False
        retry_on_result=lambda result: not result,
        wrap_exception=True
    )
    def acquire(self):
        return super(ReentrantRedLock, self).acquire()


# If multiprocessing supported non-inherited shared resources we could be dynamic and use multiprocessing's RLock
# implementation more directly. However, since it only supports inherited shared resources (created up-front in the
# parent process) we have to make our MemLock rely on a single master lock for the acquire and release operations.
# class MemLock(object):
#     _lock_map = None
#     _acquired_map = None

#     def __init__(self, key, manager):
#         self._key = key
#         self._manager = manager
#         if MemLock._lock_map is None:
#             MemLock._lock_map = self._manager.dict()
#             MemLock._acquired_map = self._manager.dict()
#         if key not in MemLock._lock_map:
#             self._lock_map[key] = self._manager.RLock()
#             self._acquired_map[key] = self._manager.Value(ctypes.c_uint, 0)
#         self._lock = self._lock_map[key]
#         self._acquired = self._acquired_map[key]

#     def acquire(self, *a, **k):
#         result = self._lock.acquire(*a, **k)
#         if result:
#             with self._acquired.get_lock():
#                 self._acquired.value += 1
#             print 'acquired'
#         return result

#     def release(self):
#         self._lock.release()
#         with self._acquired.get_lock():
#             self._acquired.value -= 1
#         print 'released'

#     def __enter__(self):
#         return self._lock.__enter__()

#     def __exit__(self, *a, **k):
#         return self._lock.__exit__(*a, **k)

class MemLock(object):
    _manager = None
    _lock_map = None
    _master_lock = None

    @classmethod
    def init(cls, manager):
        """Initialize the MemLock instance. Must be called with a multiprocessing.Manager instance
        in the parent process of all processes which will be using MemLock.

        As multiprocessing only supports shared resources created in a parent process we need
        to rely on a shared dict and lock to support our locking operations. A master lock object
        managed by a multiprocessing manager is used to be sure that only one lock instance is modifying
        the _lock_map at once. This means that concurrency is reduced as only one process can be acquiring
        or releasing a lock at once but it does allow multiple locks to be held at once, at least.
        """
        if cls._manager is not None:
            raise Error('%s already initialized' % (cls.__name__,))
        cls._manager = manager
        cls._lock_map = manager.dict()
        cls._master_lock = manager.Lock()

    def __init__(self, key):
        if self.__class__._manager is None:
            raise Error('You must call %(cls)s.init before instantiating %(cls)s' % {
                'cls': self.__class__.__name__
            })
        self._key = key

    def acquire(self):
        while True:
            lock_map = self.__class__._lock_map
            with self.__class__._master_lock:
                if self._key not in lock_map:
                    lock_map[self._key] = id(self)
                    return True
            time.sleep(0.01)

    def release(self):
        lock_map = self.__class__._lock_map
        with self.__class__._master_lock:
            if self._key not in lock_map:
                raise Error('The lock %s does not appear to be acquired yet' % (self._key,))
            if lock_map[self._key] != id(self):
                raise Error('The lock %s does not appear to have been acquired by us' % (self._key,))
            del lock_map[self._key]

    def __enter__(self):
        if not self.acquire():
            # Currently impossible
            raise Error('Could not acquire lock %s' % (self._key,))

    def __exit__(self, exc_type, exc_value, traceback):
        self.release()


class ReentrantMemLock(MemLock):
    def __init__(self, *args, **kwargs):
        super(ReentrantMemLock, self).__init__(*args, **kwargs)
        self._acquired = 0

    def acquire(self):
        if self._acquired == 0:
            result = super(ReentrantMemLock, self).acquire()
            if result:
                self._acquired += 1
            return result
        else:
            self._acquired += 1
            return True

    def release(self):
        if self._acquired > 0:
            self._acquired -= 1
            if self._acquired == 0:
                return super(ReentrantMemLock, self).release()
            return True
        return False
