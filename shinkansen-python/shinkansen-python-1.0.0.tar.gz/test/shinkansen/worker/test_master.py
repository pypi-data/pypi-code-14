import logging
import multiprocessing
import Queue
import threading
import time

import mox


log = logging.getLogger(__name__)


class MockWorker(object):
    def __init__(self, pid=0):
        self.pid = pid
        self.alive = True

    def is_alive(self):
        return self.alive

    def join(self, timeout=None):
        pass


class TestMigrationWorkerMasterBase(mox.MoxTestBase):
    def setUp(self):
        super(TestMigrationWorkerMasterBase, self).setUp()

        self.mox.StubOutWithMock(multiprocessing.Process, 'terminate')

        from shinkansen.worker import master
        self.master = master.MigrationWorkerMasterBase()

        self.mox.StubOutWithMock(master, 'time')

    def test_run_simple(self):
        self.mox.StubOutWithMock(self.master, '_start_workers')
        self.master._start_workers()
        self.mox.ReplayAll()

        thread = threading.Thread(target=self.master.run)
        thread.start()

        self.master.shutdown()
        thread.join()

    def test_run_with_worker(self):
        from shinkansen.worker import master
        self.mox.StubOutWithMock(self.master, '_start_workers')
        self.mox.StubOutWithMock(self.master, '_shutdown_workers')
        self.master._start_workers()
        self.master._shutdown_workers()
        worker = self.mox.CreateMock(multiprocessing.Process)
        worker.pid = 0
        worker.join(0)
        worker.is_alive().AndReturn(True)
        master.time.sleep(1)
        worker.join(0)
        worker.is_alive().AndReturn(False)
        self.master.workers = [worker]
        self.mox.ReplayAll()

        thread = threading.Thread(target=self.master.run)
        thread.start()

        self.master.shutdown()
        thread.join()

    def test_terminate_terminates_workers(self):
        worker = self.mox.CreateMock(multiprocessing.Process)
        self.master.workers = [worker]
        worker.is_alive().AndReturn(True)
        worker.terminate()
        multiprocessing.Process.terminate()
        self.mox.ReplayAll()

        self.master.terminate()

    def test_multiple_shutdowns(self):
        # This class sets state such that shutdown() gets called twice.
        # On the second time through the master's run() loop the worker is flagged as not alive, thus ending the thread.
        class MockEvent(object):
            def __init__(self, master, worker):
                self.master = master
                self.worker = worker
                self._set = False
                self._set_worker_dead = False

            def wait(self):
                log.debug('MockEvent.wait')
                self.master.shutdown()

            def is_set(self):
                log.debug('MockEvent.is_set %r', self._set)
                if self._set_worker_dead:
                    log.debug('MockEvent.is_set setting worker not alive')
                    self.worker.alive = False
                return self._set

            def clear(self):
                self._set = False
                log.debug('MockEvent.clear calling shutdown')
                self.master.shutdown()
                log.debug('MockEvent.clear flagging for worker death')
                self._set_worker_dead = True

            def set(self):
                log.debug('MockEvent.set')
                self._set = True

        from shinkansen.worker import master
        self.mox.StubOutWithMock(self.master, '_start_workers')
        self.mox.StubOutWithMock(self.master, '_shutdown_workers')
        self.master._start_workers()
        self.master._shutdown_workers()
        master.time.sleep(1)
        self.master._shutdown_workers()
        worker = MockWorker()
        self.master.shutdown_event = MockEvent(self.master, worker)
        self.master.workers = [worker]
        self.mox.ReplayAll()

        self.master.run()


class TestMigrationWorkerMasterMultiprocessing(mox.MoxTestBase):
    def setUp(self):
        super(TestMigrationWorkerMasterMultiprocessing, self).setUp()
        from shinkansen import config
        # TODO(jpatrin): The workers are getting imported somehow before we can reset the config here.
        # Likely the interpreter state is not being reset between tests. Should refactor so these definitions
        # don't happen at import time.
        config.QUEUE_SYSTEM = 'multiprocessing'
        from shinkansen.worker import verifier
        if not hasattr(verifier, 'VERIFY_QUEUES'):
            log.warning('verifier.VERIFY_QUEUES does not exist')
            verifier.VERIFY_QUEUES = {}
        from shinkansen.worker import pipe
        if not hasattr(pipe, 'PIPE_QUEUES'):
            log.warning('pipe.PIPE_QUEUES does not exist')
            pipe.PIPE_QUEUES = {}

    def test_shutdown_workers_graceful(self):
        from shinkansen.worker import master
        master.queue_migration_queue = {
            'a': self.mox.CreateMockAnything(),
            'b': self.mox.CreateMockAnything(),
        }
        master.EXPORT_QUEUES = {
            'a': self.mox.CreateMockAnything(),
            'b': self.mox.CreateMockAnything(),
        }
        master.shutdown_export_event = self.mox.CreateMockAnything()
        master.stream_queue = self.mox.CreateMockAnything()
        master.shutdown_stream_event = self.mox.CreateMockAnything()
        master.import_queue = self.mox.CreateMockAnything()
        master.shutdown_import_event = self.mox.CreateMockAnything()
        for queue in master.queue_migration_queue.values():
            queue.join()
        for queue in master.EXPORT_QUEUES.values():
            queue.join()
        master.shutdown_export_event.set()
        master.stream_queue.join()
        master.shutdown_stream_event.set()
        master.import_queue.join()
        master.shutdown_import_event.set()
        self.mox.ReplayAll()

        master.MigrationWorkerMasterMultiprocessing()._shutdown_workers()

    def test_shutdown_workers_quick(self):
        from shinkansen.worker import master
        master.queue_migration_queue = {
            'a': self.mox.CreateMockAnything(),
            'b': self.mox.CreateMockAnything()
        }
        master.EXPORT_QUEUES = {
            'a': self.mox.CreateMockAnything(),
            'b': self.mox.CreateMockAnything()
        }
        master.shutdown_export_event = self.mox.CreateMockAnything()
        master.stream_queue = self.mox.CreateMockAnything()
        master.shutdown_stream_event = self.mox.CreateMockAnything()
        master.import_queue = self.mox.CreateMockAnything()
        master.shutdown_import_event = self.mox.CreateMockAnything()

        for shutdown_event, queues in [
            (master.shutdown_export_event, master.queue_migration_queue.values() + master.EXPORT_QUEUES.values()),
            (master.shutdown_stream_event, [master.stream_queue]),
            (master.shutdown_import_event, [master.import_queue])
        ]:
            shutdown_event.set()
            for queue in queues:
                queue.get(block=False)
                queue.get(block=False).AndRaise(Queue.Empty())

        import signal
        int_worker = MockWorker(1)
        kill_worker = MockWorker(2)
        dead_worker = MockWorker(3)
        workers = {
            1: (signal.SIGINT, int_worker),
            2: (signal.SIGKILL, kill_worker),
        }
        class MockProcess(object):
            def __init__(self, pid):
                if pid in workers:
                    self._signal, self.worker = workers[pid]
                else:
                    raise psutil.NoSuchProcess(pid)

            def send_signal(self, signal):
                if signal == self._signal:
                    self.worker.alive = False

        import psutil
        psutil.Process = MockProcess

        self.mox.StubOutWithMock(time, 'sleep')
        time.sleep(1)

        self.mox.ReplayAll()

        worker_master = master.MigrationWorkerMasterMultiprocessing()
        worker_master.workers = [int_worker, kill_worker, dead_worker]
        worker_master.graceful_shutdown = False
        worker_master._shutdown_workers()


class TestMigrationWorkerMasterCelery(mox.MoxTestBase):
    def setUp(self):
        super(TestMigrationWorkerMasterCelery, self).setUp()
        from shinkansen import config
        config.QUEUE_SYSTEM = 'celery'

    def test_shutdown_workers_gracefully(self):
        w1 = self.mox.CreateMock(multiprocessing.Process)
        w1.is_alive().AndReturn(True)
        w1.terminate()
        w2 = self.mox.CreateMock(multiprocessing.Process)
        w2.is_alive().AndReturn(False)

        self.mox.ReplayAll()

        from shinkansen.worker import master
        worker_master = master.MigrationWorkerMasterCelery()
        worker_master.workers = [w1, w2]
        worker_master._shutdown_workers()

    def test_shutdown_workers_quickly(self):
        import psutil
        import signal
        psutil.Process = self.mox.CreateMockAnything()
        w1 = self.mox.CreateMock(multiprocessing.Process)
        w1.pid = 1
        w1.is_alive().AndReturn(True)
        p1 = self.mox.CreateMockAnything()
        psutil.Process(w1.pid).AndReturn(p1)
        p1.send_signal(signal.SIGQUIT)
        w2 = self.mox.CreateMock(multiprocessing.Process)
        w2.pid = 2
        w2.is_alive().AndReturn(False)
        w3 = self.mox.CreateMock(multiprocessing.Process)
        w3.pid = 3
        w3.is_alive().AndReturn(True)
        psutil.Process(w3.pid).AndRaise(psutil.NoSuchProcess(w3.pid))

        self.mox.ReplayAll()

        from shinkansen.worker import master
        worker_master = master.MigrationWorkerMasterCelery()
        worker_master.workers = [w1, w2, w3]
        worker_master.graceful_shutdown = False
        worker_master._shutdown_workers()
