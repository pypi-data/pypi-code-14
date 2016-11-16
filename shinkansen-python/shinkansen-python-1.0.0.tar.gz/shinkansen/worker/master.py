import logging
import multiprocessing
import os
import Queue
import random
import signal
import socket
import time

import flower.command
import psutil

import shinkansen.db
from shinkansen import config, orm
from shinkansen.worker import (
    shutdown_export_event,
    stream_queue, archive_queue, shutdown_stream_event,
    import_queue, shutdown_import_event,
    queue_migration_queue,
    celery_app
)
from shinkansen.worker.queuer import QueueChunksWorkerMysql, QueueChunksWorkerCrate
from shinkansen.worker.exporter import ExportChunkWorker, EXPORT_QUEUES
from shinkansen.worker.streamer import StreamChunkWorker, ArchiveChunkWorker
from shinkansen.worker.importer import ImportChunkWorker
from shinkansen.worker import pipe, verifier


log = logging.getLogger(__name__)


def worker_loop(cls, work_queue, shutdown_event, source_shard=None):
    log.info('Worker %s-%s starting up', cls.__name__ + ('' if source_shard is None else ('-' + source_shard)),
             os.getpid())
    with shinkansen.db.redis_conn() as redis:
        worker = orm.Worker(redis)
        worker.host = socket.gethostname()
        worker.pid = os.getpid()
        worker.type = cls.__name__
        worker.status = 'idle'
        worker.source_shard = source_shard
        worker.insert()
        try:
            while not shutdown_event.is_set():
                try:
                    try:
                        chunk_config = work_queue.get(timeout=1 + random.random())
                    except Queue.Empty:
                        worker.update()
                        continue
                    try:
                        worker.migration_id = chunk_config.migration_id
                        worker.partition_val = chunk_config.partition_val
                        worker.namespace = chunk_config.namespace
                        worker.table_name = chunk_config.table_config.table_name if chunk_config.table_config else None
                        worker.chunk_num = chunk_config.chunk_num
                        worker.source_shard = chunk_config.source_shard
                        worker.destination_shard = chunk_config.destination_shard
                        worker.status = 'running'
                        worker.update()

                        cls(chunk_config, redis).run()
                    except Exception:
                        log.exception('Exception from worker, putting this chunk back on the queue after sleeping')
                        time.sleep(10 + random.randint(0, 10))
                        work_queue.put(chunk_config)
                    finally:
                        work_queue.task_done()

                        worker.migration_id = None
                        worker.partition_val = None
                        worker.table_name = None
                        worker.chunk_num = None
                        worker.source_shard = source_shard
                        worker.destination_shard = None
                        worker.status = 'idle'
                        worker.update()
                except Exception:
                    log.exception('?')
                    time.sleep(10 + random.randint(0, 10))
        finally:
            worker.delete()
    log.info('Worker %s-%s shutting down', cls.__name__, os.getpid())


class MigrationWorkerMasterBase(multiprocessing.Process):
    def __init__(self):
        super(MigrationWorkerMasterBase, self).__init__(name='MigrationWorkerMaster')
        self.workers = []
        self.shutdown_event = multiprocessing.Event()
        self.graceful_shutdown = True

    def run(self):
        log.debug('Starting workers')
        self._start_workers()
        log.debug('Waiting for self.shutdown_event')
        self.shutdown_event.wait()
        while len(self.workers) > 0:
            if self.shutdown_event.is_set():
                self.shutdown_event.clear()
                log.debug('Shutting down workers')
                self._shutdown_workers()
            log.debug('Joining workers')
            workers = []
            for worker in self.workers:
                log.debug('Joining worker %r', worker.pid)
                worker.join(0)
                if not worker.is_alive():
                    continue
                workers.append(worker)
            self.workers = workers
            if len(self.workers) > 0:
                time.sleep(1)

    def terminate(self):
        # terminate any living workers
        for worker in self.workers:
            if worker.is_alive():
                worker.terminate()
        super(MigrationWorkerMasterBase, self).terminate()

    def shutdown(self, graceful=True):
        # Once graceful has been set as False, don't set it back
        if self.graceful_shutdown and not graceful:
            self.graceful_shutdown = graceful
        if not self.shutdown_event.is_set():
            log.debug('Setting self.shutdown_event')
            self.shutdown_event.set()

    # Interface
    def _start_workers(self):
        raise NotImplementedError()

    def _shutdown_workers(self):
        raise NotImplementedError()


def QueueChunksWorker(chunk_config, redis):
    if chunk_config.source_type == 'mysql':
        return QueueChunksWorkerMysql(chunk_config, redis)
    elif chunk_config.source_type == 'crate':
        return QueueChunksWorkerCrate(chunk_config, redis)


class MigrationWorkerMasterMultiprocessing(MigrationWorkerMasterBase):
    def _start_workers(self):
        # non-shard-specific workers
        worker_configs = [
            (config.NUM_STREAM_WORKERS, (StreamChunkWorker, stream_queue, shutdown_stream_event)),
            (config.NUM_ARCHIVE_WORKERS, (ArchiveChunkWorker, archive_queue, shutdown_stream_event)),
        ]
        if config.RUN_IMPORT_WORKERS:
            worker_configs.append(
                (config.NUM_IMPORT_WORKERS, (ImportChunkWorker, import_queue, shutdown_import_event))
            )
        # shard-specific workers
        for shards, shard_worker_configs in [
            (config.SOURCES, [
                (config.NUM_EXPORT_WORKERS, ExportChunkWorker,
                 EXPORT_QUEUES, shutdown_export_event),
                (config.NUM_QUEUE_MIGRATION_WORKERS, QueueChunksWorker,
                 queue_migration_queue, shutdown_export_event),
                (config.NUM_PIPE_WORKERS, pipe.PipeChunkWorker,
                 pipe.PIPE_QUEUES, shutdown_export_event),
            ]),
            (config.DESTINATIONS, [
                (config.NUM_VERIFICATION_WORKERS, verifier.VerifyWorker,
                 verifier.VERIFY_QUEUES, shutdown_import_event)
            ])
        ]:
            shard_workers = {}
            for shard_config in shards.values():
                queue_key = shard_config['config']['queue_key']
                if queue_key in shard_workers:
                    continue
                shard_workers[queue_key] = True
                for (num_workers, worker_class, worker_queue, worker_event) in shard_worker_configs:
                    worker_configs.append(
                        (num_workers, (worker_class, worker_queue[queue_key], worker_event, queue_key)))
        # start the processes
        for (num_workers, worker_args) in worker_configs:
            for _ in xrange(num_workers):
                worker = multiprocessing.Process(target=worker_loop, args=worker_args)
                worker.daemon = True
                worker.start()
                self.workers.append(worker)

    def _shutdown_workers(self):
        if self.graceful_shutdown:
            log.debug('Joining queue migration queues')
            for shard_queue_migration_queue in queue_migration_queue.values():
                shard_queue_migration_queue.join()
            log.debug('Joining shard export queues')
            for shard_export_queue in EXPORT_QUEUES.values():
                shard_export_queue.join()
            log.debug('Setting shutdown_export_event')
            shutdown_export_event.set()
            log.debug('Joining stream_queue')
            stream_queue.join()
            log.debug('Setting shutdown_stream_event')
            shutdown_stream_event.set()
            if config.RUN_IMPORT_WORKERS:
                log.debug('Joining import_queue')
                import_queue.join()
            log.debug('Joining verifier queues')
            for verifier_queue in verifier.VERIFY_QUEUES.values():
                verifier_queue.join()
            log.debug('Setting shutdown_import_event')
            shutdown_import_event.set()
        else:
            # set all of the shutdown events and empty all of the queues
            for shutdown_event, queues in [
                (
                    shutdown_export_event,
                    (queue_migration_queue.values()
                     + EXPORT_QUEUES.values()
                     + pipe.PIPE_QUEUES.values())
                ),
                (shutdown_stream_event, [stream_queue]),
                (shutdown_import_event, [import_queue] + verifier.VERIFY_QUEUES.values())
            ]:
                shutdown_event.set()
                for queue in queues:
                    while True:
                        try:
                            queue.get(block=False)
                        except Queue.Empty:
                            break
            # send a SIGINT to all workers to make them quit quickly
            for worker in self.workers:
                if worker.is_alive():
                    try:
                        proc = psutil.Process(worker.pid)
                        proc.send_signal(signal.SIGINT)
                    except psutil.NoSuchProcess:
                        pass
            slept = False
            for worker in self.workers:
                if worker.is_alive():
                    if not slept:
                        time.sleep(1)
                        slept = True
                    try:
                        proc = psutil.Process(worker.pid)
                        proc.send_signal(signal.SIGKILL)
                    except psutil.NoSuchProcess:
                        pass
                    worker.join()


def start_celery_worker(argv):
    celery_app.worker_main(argv)


def start_flower_worker():
    flower.command.FlowerCommand().execute_from_commandline(['flower'])


class MigrationWorkerMasterCelery(MigrationWorkerMasterBase):
    def _start_workers(self):
        # TODO(jpatrin): CM-413: Need to combine workers for queuer, exporter, importer, and verifier for a single shard
        worker_configs = [
            ('streamer', 'stream_chunk', config.NUM_STREAM_WORKERS),
            ('archiver', 'archive_chunk_%s' % (socket.gethostname(),), config.NUM_ARCHIVE_WORKERS),
        ]
        if config.RUN_IMPORT_WORKERS:
            worker_configs.append(
                ('importer', 'import_chunk', config.NUM_IMPORT_WORKERS)
            )
        for shards, shard_worker_configs in [
            (config.SOURCES, [
                ('queuer_%s', 'start_migration_%s', config.NUM_QUEUE_MIGRATION_WORKERS),
                ('exporter_%s', 'export_chunk_%s', config.NUM_EXPORT_WORKERS),
                ('pipe_%s', 'pipe_%s', config.NUM_PIPE_WORKERS),
            ]),
            (config.DESTINATIONS, [
                ('verifier_%s', 'verify_%s', config.NUM_VERIFICATION_WORKERS),
            ])
        ]:
            shard_workers = {}
            for shard_config in shards.values():
                queue_key = shard_config['config']['queue_key']
                if queue_key in shard_workers:
                    continue
                shard_workers[queue_key] = True
                for (worker_name, worker_queue, num_workers) in shard_worker_configs:
                    worker_configs.append(
                        (worker_name % (queue_key,), worker_queue % (queue_key,), num_workers))

        for (name, queue, num_workers) in worker_configs:
            for i in range(num_workers):
                argv = [
                    'worker',
                    '--loglevel=info',
                    '--hostname=%s.%%h' % (name + '_' + str(i),),
                    '--queues=shinkansen.worker.%s' % (queue,),
                    '--concurrency=%u' % (1,),
                    '--heartbeat-interval=30',
                ]
                proc = multiprocessing.Process(target=start_celery_worker, args=(argv,))
                proc.start()
                self.workers.append(proc)
                time.sleep(0.2)
        proc = multiprocessing.Process(target=start_flower_worker)
        proc.start()
        self.workers.append(proc)

    def _shutdown_workers(self):
        if self.graceful_shutdown:
            for worker in self.workers:
                if worker.is_alive():
                    worker.terminate()
        else:
            log.debug('Sending SIGQUIT to workers')
            for worker in self.workers:
                if worker.is_alive():
                    try:
                        log.debug('Sending SIGQUIT to %r', worker.pid)
                        proc = psutil.Process(worker.pid)
                        proc.send_signal(signal.SIGQUIT)
                    except psutil.NoSuchProcess:
                        pass


if config.QUEUE_SYSTEM == 'multiprocessing':
    MigrationWorkerMaster = MigrationWorkerMasterMultiprocessing
elif config.QUEUE_SYSTEM == 'celery':
    MigrationWorkerMaster = MigrationWorkerMasterCelery
