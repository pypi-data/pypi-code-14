import multiprocessing

from shinkansen import config, worker
from shinkansen.worker.exporter import mysql, crate


EXPORT_QUEUES = {}
EXPORT_TASKS = {}


def _queue_export_chunk_multiprocessing(chunk_config):
    EXPORT_QUEUES[
        config.SOURCES[chunk_config.source_shard]['config']['queue_key']
    ].put(chunk_config)


def _queue_export_chunk_celery(chunk_config):
    EXPORT_TASKS[
        config.SOURCES[chunk_config.source_shard]['config']['queue_key']
    ].delay(chunk_config)


# Masquerade as a class, but this is just a shim to get the right class for the source shard type
def ExportChunkWorker(chunk_config, redis_conn):
    if chunk_config.source_type == 'mysql':
        return mysql.ExportChunkWorkerMysql(chunk_config, redis_conn)
    elif chunk_config.source_type == 'crate':
        return crate.ExportChunkWorkerCrate(chunk_config, redis_conn)


if config.QUEUE_SYSTEM == 'multiprocessing':
    for _shard_config in config.SOURCES.values():
        if _shard_config['config']['queue_key'] in EXPORT_QUEUES:
            continue
        EXPORT_QUEUES[_shard_config['config']['queue_key']] = multiprocessing.JoinableQueue()

    def queue_export_chunk(chunk_config):
        EXPORT_QUEUES[
            config.SOURCES[chunk_config.source_shard]['config']['queue_key']
        ].put(chunk_config)

elif config.QUEUE_SYSTEM == 'celery':
    for _shard_config in config.SOURCES.values():
        if _shard_config['config']['queue_key'] in EXPORT_TASKS:
            continue
        EXPORT_TASKS[_shard_config['config']['queue_key']] = worker.celery_app.task(
            bind=True,
            name='shinkansen.worker.export_chunk_' + _shard_config['config']['queue_key']
        )(worker.migration_task_wrapper(ExportChunkWorker))

    def queue_export_chunk(chunk_config):
        EXPORT_TASKS[
            config.SOURCES[chunk_config.source_shard]['config']['queue_key']
        ].delay(chunk_config)
