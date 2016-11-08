'''
Copyright (C) 2015-2016 Skylable Ltd. <info-copyright@skylable.com>
License: Apache 2.0, see LICENSE for more details.
'''

from __future__ import unicode_literals

import traceback
from typing import Callable, Any, List  # noqa
from threading import Thread

from six.moves import range, queue  # type: ignore


DEFAULT_JOIN_TIMEOUT = 0.5


class ThreadQueue(queue.Queue):
    unfinished_tasks = None  # type: int

    def clear(self):
        # type: () -> None
        # A bit modified version of:
        # http://stackoverflow.com/questions/6517953/clear-all-items-from-the-queue  # noqa
        with self.mutex:
            unfinished = self.unfinished_tasks - len(self.queue)
            if unfinished < 0:
                raise ValueError('task_done() called too many times')
            self.unfinished_tasks = unfinished
            self.queue.clear()
            if unfinished == 0:
                self.all_tasks_done.notify_all()
            self.not_full.notify_all()


class ThreadPoolWorker(object):
    def __init__(self, thread_pool):
        # type: (ThreadPool) -> None
        self.thread_pool = thread_pool
        self._running = False

    def is_running(self):
        # type: () -> bool
        return self._running

    def set_running(self, value):
        # type: (bool) -> None
        self._running = value

    def run(self):
        # type: () -> None
        self.set_running(True)
        while self.is_running():
            try:
                func, args, kwargs = self.thread_pool._queue.get(
                    timeout=DEFAULT_JOIN_TIMEOUT
                )
            except queue.Empty:
                continue

            try:
                func(*args, **kwargs)
            except Exception:
                traceback.print_exc()
            finally:
                self.thread_pool._queue.task_done()


class ThreadPool(object):
    def __init__(self, threads_no, max_task_queue_size=0):
        # type: (int, int) -> None
        self._queue = ThreadQueue(max_task_queue_size)
        self._threads_no = threads_no
        self._workers = [
            ThreadPoolWorker(self) for _ in range(self._threads_no)
        ]
        self._threads = []  # type: List[Thread]

    def __enter__(self):
        # type: () -> ThreadPool
        self.start()
        return self

    def __exit__(self, type, value, traceback):
        # type: (Any, Any, Any) -> None
        self.stop()

    def start(self):
        # type: () -> None
        if self._threads:
            raise RuntimeError(
                'ThreadPool already running! Call .stop() method first.'
            )
        for worker in self._workers:
            thread = Thread(target=worker.run)
            thread.daemon = True
            thread.start()
            self._threads.append(thread)

    def wait_for_completion(self):
        # type: () -> None
        self._queue.join()

    def stop(self):
        # type: () -> None
        if not self._threads:
            raise RuntimeError(
                'ThreadPool is not running.'
            )
        self.wait_for_completion()
        for worker in self._workers:
            worker.set_running(False)

        while self._threads:
            for thread in self._threads:
                thread.join(timeout=DEFAULT_JOIN_TIMEOUT)
                if not thread.is_alive():
                    self._threads.remove(thread)
                    break

    def process_task(self, func, *args, **kwargs):
        # type: (Callable, *Any, **Any) -> None
        self._queue.put((func, args, kwargs))

    def clear_task_queue(self):
        # type: () -> None
        self._queue.clear()
