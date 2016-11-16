from datetime import datetime
import threading
import time

from flask.ext import restful
from flask.json import jsonify
from flask_restful import reqparse
import requests

import shinkansen
from shinkansen import config, db, orm, UnrecoverableError
from shinkansen.http import common
import shinkansen.status
from shinkansen.worker import queuer


# TODO: Add auto, complete, and initial endpoints to the REST links entries

class Resource(restful.Resource):
    method_decorators = [common.keyed]


class Root(Resource):
    VERSION = 5

    def get(self):
        return {
            'version': self.VERSION,
            'links': [
                {
                    'href': '/v5/sources',
                    'rel': 'list',
                    'method': 'GET',
                },
                {
                    'href': '/v5/health',
                    'rel': 'health',
                    'method': 'GET',
                },
            ],
        }


def get_migration_status(migration_id):
    with db.redis_conn() as redis_conn:
        migration = orm.Migration.get(redis_conn, migration_id=migration_id)
    if migration is None:
        return None
    return _get_migration_status(migration)


def _get_migration_status(migration):
    computed_status = shinkansen.status.get_migration_status(migration_id=migration.migration_id)

    uri_base = '/v5/migration/%s/' % (migration.migration_id,)
    result = {
        'migration_id': migration.migration_id,
        'type': migration.type,
        'source': migration.source_shard,
        'destination': migration.destination_shard,
        'namespace': migration.namespace,
        'status': migration.status,
        'status_code': common.STATUS_CODES[migration.status],
        'partition_val': migration.partition_val,
        'verification_status': migration.verification_status,
        'computed_status': computed_status.computed_status,
        'computed_status_code': common.STATUS_CODES[computed_status.computed_status],
        'computed_verification_status': computed_status.computed_verification_status,
        'start_time': migration.start_time,
        'end_time': migration.end_time,
    }
    if computed_status.computed_status != 'not_started':
        result['links'] = [
            {
                'href': uri_base + 'tables',
                'rel': 'tables',
                'method': 'GET',
            },
        ]

    if migration.type in orm.MigrationType.__CONTAINER_TYPES__:
        result['submigrations'] = []
        for submigration in migration.get_submigrations():
            result['submigrations'].append(_get_migration_status(submigration))

    for key, num in computed_status.chunk_statuses.items():
        result['chunks_%s' % (key,)] = num
    for key, num in computed_status.table_statuses.items():
        result['tables_%s' % (key,)] = num
    for key, num in computed_status.table_verification_statuses.items():
        if key:
            result['table_verifications_%s' % (key,)] = num
    #errors = []
    #if migration.status != computed_status.computed_status:
    #    errors.append(
    #        'Computed status is not the same as the migration status. '
    #        'There may be a bug if this persists %r != %r' % (
    #            computed_status.computed_status, migration.status))
    #if migration.verification_status != computed_status.computed_verification_status:
    #    errors.append(
    #        'Computed verification status is not the same as the migration verification status. '
    #        'There may be a bug if this persists %r != %r' % (
    #            computed_status.computed_verification_status, migration.verification_status))
    #if errors:
    #    result['errors'] = errors
    return result


class Migration(Resource):
    def get(self, migration_id):
        result = get_migration_status(migration_id)
        if result is None:
            response = jsonify({'error': 'Migration %r not found' % (migration_id,)})
            response.status_code = 404
            return response

        if 'errors' in result:
            response = jsonify(result)
            response.status_code = 500
        else:
            response = result
        return response


class MigrationTables(Resource):
    def get(self, migration_id):
        with db.redis_conn() as redis_conn:
            migration = orm.Migration.get(redis_conn, migration_id=migration_id)
        if migration is None:
            response = jsonify({'error': 'Migration %r not found' % (migration_id,)})
            response.status_code = 404
            return response
        tables = shinkansen.status.get_table_migration_status(migration_id=migration_id)
        return {
            'migration_id': migration_id,
            'type': migration.type,
            'source': migration.source_shard,
            'destination': migration.destination_shard,
            'namespace': migration.namespace,
            'partition_val': migration.partition_val,
            'start_time': migration.start_time,
            'end_time': migration.end_time,
            'tables': tables,
        }


class Sources(Resource):
    def get(self):
        return {
            'sources': [
                {
                    'name': shard_name,
                    'href': '/v5/source/%s' % (shard_name,),
                }
                for shard_name in config.SOURCES
            ],
        }


class Source(Resource):
    def get(self, source):
        return {
            'name': source,
            'links': [
                {
                    'name': 'destinations',
                    'href': '/v5/source/%s/destinations' % (source,)
                },
            ],
        }


class SourceDestinations(Resource):
    def get(self, source):
        return {
            'name': source,
            'destinations': [
                {
                    'name': name,
                    'href': '/v5/source/destination/%s' % (name,),
                } for name in config.DESTINATIONS
            ],
        }


def get_migrations_dict(source, destination, partition_val, migration_type=None):
    with db.redis_conn() as redis_conn:
        clauses = {
            'source_shard': source,
            'destination_shard': destination,
            'partition_val': partition_val,
        }
        if migration_type is not None:
            clauses['type'] = migration_type
        migrations = orm.Migration.get_by_index(
            redis_conn,
            **clauses)
    return {
        'source': source,
        'destination': destination,
        'partition_val': partition_val,
        'migrations': [
            get_migration_status(migration.migration_id)
            for migration in migrations
        ],
    }


def strbool(s):
    return bool(s) and s.lower() != 'false' and s.lower() != 'f' and s != '0'


def start_migration(source, destination, partition_val, migration_type):
    parser = reqparse.RequestParser()
    parser.add_argument('namespace', type=str, help='the namespace to prefix the schema with', default='')
    parser.add_argument('requeue', type=strbool, help='requeue migrations')
    parser.add_argument('force', type=strbool, help='force re-migration (will not delete existing data)')
    parser.add_argument('wanted_delta_start', type=int, help='wanted delta start timestamp in seconds')
    parser.add_argument('wanted_delta_end', type=int, help='wanted delta end timestamp in seconds')
    parser.add_argument(
        'chunk_migration_type', type=str, help='indirect or direct',
        default=orm.ChunkMigrationType.INDIRECT
    )
    args = parser.parse_args()
    if args['chunk_migration_type'] not in orm.ChunkMigrationType.__ALL__:
        raise UnrecoverableError('chunk_migration_type %r is not valid' % (args['chunk_migration_type'],))
    if (
        migration_type not in orm.MigrationType.__DELTA_TYPES__
        and (args['wanted_delta_start'] is not None or args['wanted_delta_end'] is not None)
    ):
        return {'error': 'wanted_delta_start and wanted_delta_end are only allowed for delta migration types'}
    (migration, tables) = queuer.migrate_partition_shard(
        partition_val, args['namespace'], source, destination,
        force=args['force'], requeue=args['requeue'], migration_type=migration_type,
        wanted_delta_start=args['wanted_delta_start'],
        wanted_delta_end=args['wanted_delta_end'],
        chunk_migration_type=args['chunk_migration_type']
    )
    response = {
        'migration_id': migration.migration_id,
        'source': source,
        'destination': destination,
        'namespace': args['namespace'],
        'links': [
            {
                'href': '/v5/migration/%s' % (migration.migration_id,),
                'rel': 'migration',
                'method': 'GET',
            }
        ],
        'tables': {},
    }
    error = False
    for table_name, table in tables.iteritems():
        if table is None:
            response['tables'][table_name] = {
                'status': 'error',
                'error': 'Table was not queued due to it being either in progress or previously migrated',
            }
            error = True
        else:
            response['tables'][table_name] = {'status': table.status}
    if error:
        response['error'] = 'Not all tables were queued.'
    return response


class SourceDestination(Resource):
    def get(self, source, destination):
        response = get_migrations_dict(source, destination, 'ALL')
        response['links'] = [
            {
                'href': '/v5/source/' + source + '/destination/' + destination + '/latest',
                'rel': 'migration',
                'method': 'GET',
            }
        ]
        return response

    def post(self, source, destination):
        return start_migration(source, destination, 'ALL', orm.MigrationType.FULL)


class SourceDestinationFull(Resource):
    def get(self, source, destination):
        return get_migrations_dict(source, destination, 'ALL', orm.MigrationType.FULL)

    def post(self, source, destination):
        return start_migration(source, destination, 'ALL', orm.MigrationType.FULL)


class SourceDestinationLatest(Resource):
    def get(self, source, destination):
        with db.redis_conn() as redis:
            migration = orm.Migration.get_latest(
                redis, source_shard=source, destination_shard=destination, partition_val='ALL')
        if migration is None:
            response = jsonify({'error': 'No migrations found'})
            response.status_code = 404
            return response
        return Migration().get(migration_id=migration.migration_id)


class SourceDestinationDelta(Resource):
    def get(self, source, destination):
        return get_migrations_dict(source, destination, 'ALL', orm.MigrationType.DELTA)

    def post(self, source, destination):
        return start_migration(source, destination, 'ALL', orm.MigrationType.DELTA)


class SourceDestinationDeltaAuto(Resource):
    def get(self, source, destination, partition_val):
        return get_migrations_dict(source, destination, 'ALL', orm.MigrationType.AUTODELTA)

    def post(self, source, destination):
        return start_migration(source, destination, 'ALL', orm.MigrationType.AUTODELTA)


class SourceDestinationComplete(Resource):
    def get(self, source, destination):
        return get_migrations_dict(source, destination, 'ALL', orm.MigrationType.COMPLETE)

    def post(self, source, destination):
        return start_migration(source, destination, 'ALL', orm.MigrationType.COMPLETE)


class SourceDestinationPartitions(Resource):
    def get(self, source, destination):
        with db.redis_conn() as redis:
            partition_vals = set(
                rec[0] for rec in
                orm.Migration.get_columns(redis, columns=['partition_val'])
            )
        return {
            'partitions': [
                {
                    'id': partition_val,
                    'href': '/v5/source/%s/destination/%s/partition/%s' % (source, destination, partition_val),
                    'source': source,
                    'destination': destination,
                }
                for partition_val in partition_vals
            ],
        }


class SourceDestinationPartition(Resource):
    def get(self, source, destination, partition_val):
        response = get_migrations_dict(source, destination, partition_val)
        response['links'] = [
            {
                'href': ('/v5/source/' + str(source) + '/destination/' + str(destination) +
                         '/partition/' + str(partition_val) + '/latest'),
                'rel': 'migration',
                'method': 'GET',
            }
        ]
        return response

    def post(self, source, destination, partition_val):
        return start_migration(source, destination, partition_val, orm.MigrationType.FULL)


class SourceDestinationPartitionFull(Resource):
    def get(self, source, destination, partition_val):
        response = get_migrations_dict(source, destination, partition_val, orm.MigrationType.FULL)
        response['links'] = [
            {
                'href': ('/v5/source/' + str(source) + '/destination/' + str(destination) +
                         '/partition/' + str(partition_val) + '/latest'),
                'rel': 'migration',
                'method': 'GET',
            }
        ]
        return response

    def post(self, source, destination, partition_val):
        return start_migration(source, destination, partition_val, orm.MigrationType.FULL)


class SourceDestinationPartitionLatest(Resource):
    def get(self, source, destination, partition_val):
        with db.redis_conn() as redis:
            migration = orm.Migration.get_latest(
                redis, source_shard=source, destination_shard=destination, partition_val=partition_val)
        if migration is None:
            response = jsonify({'error': 'No migrations found'})
            response.status_code = 404
            return response
        return Migration().get(migration_id=migration.migration_id)


class SourceDestinationPartitionDelta(Resource):
    def get(self, source, destination, partition_val):
        return get_migrations_dict(source, destination, partition_val, orm.MigrationType.DELTA)

    def post(self, source, destination, partition_val):
        return start_migration(source, destination, partition_val, orm.MigrationType.DELTA)


class SourceDestinationPartitionDeltaAuto(Resource):
    def get(self, source, destination, partition_val):
        return get_migrations_dict(source, destination, partition_val, orm.MigrationType.AUTODELTA)

    def post(self, source, destination, partition_val):
        return start_migration(source, destination, partition_val, orm.MigrationType.AUTODELTA)


class SourceDestinationPartitionComplete(Resource):
    def get(self, source, destination, partition_val):
        return get_migrations_dict(source, destination, partition_val, orm.MigrationType.COMPLETE)

    def post(self, source, destination, partition_val):
        return start_migration(source, destination, partition_val, orm.MigrationType.COMPLETE)


class Health(Resource):
    def get(self):
        return {
            'status_code': 0,
            'status': 'ok',
            'links': [
                {
                    'href': '/v5/health/queues',
                    'rel': 'queues',
                    'method': 'GET',
                },
                {
                    'href': '/v5/health/chunks',
                    'rel': 'chunks',
                    'method': 'GET',
                },
                {
                    'href': '/v5/health/database',
                    'rel': 'database',
                    'method': 'GET',
                },
                {
                    'href': '/v5/health/stuck',
                    'rel': 'stuck',
                    'method': 'GET',
                },
            ],
        }


class QueueHealth(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            'all', type=strbool, help='return all queues, default is to return only those with messages')
        args = parser.parse_args()
        resp = requests.get(
            'http://%s:%i/api/queues' % (config.RABBITMQ_HOST, config.RABBITMQ_MANAGEMENT_PORT),
            auth=('guest', 'guest')
        )
        data = resp.json()
        queues = {
            queue['name']: queue['messages']
            for queue in data
            if queue['name'].startswith('shinkansen.') and (args['all'] or queue['messages'] > 0)
        }
        return queues


class ChunkHealth(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('cutoff', type=int, help='cutoff timestamp in ms')
        parser.add_argument('full', type=strbool, help='show all columns')
        args = parser.parse_args()
        if args['cutoff'] is None:
            cutoff = (time.time() - 14 * 24 * 60 * 60) * 1000
        else:
            cutoff = args['cutoff']
        with db.redis_conn() as red:
            chunks = []
            for status in ['migrating', 'converting', 'importing', 'exporting']:
                chunks.extend(orm.Chunk.get_by_index(red, status=status))
            running_chunks = [c for c in chunks if c.queued_time > cutoff]
            if not running_chunks:
                return []

            cols = [
                'queued_time',
                'partition_val',
                'source_shard',
                'table_name',
                'chunk_num',
                'num_records_exported',
                'num_records_converted',
                'num_records_imported',
                'status'
            ] if not args['full'] else running_chunks[0]._cols()

            date_cols = ['queued_time', 'start_time', 'end_time']
            result = []
            for chunk in running_chunks:
                rchunk = {}
                for col in cols:
                    value = getattr(chunk, col)
                    if col in date_cols:
                        rchunk[col] = None if value is None else str(datetime.fromtimestamp(value // 1000))
                    else:
                        rchunk[col] = value
                result.append(rchunk)
            result.sort(key=lambda t: (t['partition_val'], t['source_shard'], t['table_name'], t['chunk_num']))
            return result


class DatabaseHealth(Resource):
    MAX_TIME = 5
    check_threads = {}
    check_thread_lock = threading.Lock()

    def __init__(self):
        self.result = None
        self.result_lock = threading.Lock()

    def check_shard(self, shard):
        start_time = time.time()
        try:
            with db.shard_connection(shard, read=False) as conn:
                conn.check_health()
            with self.result_lock:
                if shard not in self.result['databases']:
                    self.result['databases'][shard] = {
                        'ms': int((time.time() - start_time) * 1000),
                        'status': 'ok',
                    }
        except Exception, exc:
            with self.result_lock:
                if shard not in self.result['databases']:
                    self.result['databases'][shard] = {
                        'ms': int((time.time() - start_time) * 1000),
                        'status': 'error',
                        'error': 'Exception checking shard %r' % (exc,)
                    }

    def get(self):
        for shard, thread in self.check_threads.items():
            with self.check_thread_lock:
                thread.join(0.001)
                if not thread.is_alive():
                    del self.check_threads[shard]
        my_check_threads = {}
        self.result = {'databases': {}}
        start_time = time.time()
        for shard in config.MYSQL_HOSTS.keys() + config.CRATE_CLUSTERS.keys():
            shard_start_time = time.time()
            with self.result_lock:
                if shard in self.check_threads:
                    self.result['databases'][shard] = {
                        'ms': int((time.time() - shard_start_time) * 1000),
                        'status': 'error',
                        'error': 'previous check is still ongoing',
                    }
                    continue
            thread = threading.Thread(target=self.check_shard, args=(shard,))
            thread.start()
            my_check_threads[shard] = thread
            self.check_threads[shard] = thread
        while (time.time() - start_time) < self.MAX_TIME and my_check_threads:
            for shard, thread in my_check_threads.items():
                with self.check_thread_lock:
                    thread.join(0.001)
                    if not thread.is_alive():
                        del my_check_threads[shard]
                        del self.check_threads[shard]
                        continue
        for shard, thread in my_check_threads.items():
            with self.check_thread_lock:
                thread.join(0.001)
                if not thread.is_alive():
                    del my_check_threads[shard]
                    del self.check_threads[shard]
                with self.result_lock:
                    if shard not in self.result['databases']:
                        self.result['databases'][shard] = {
                            'ms': int((time.time() - start_time) * 1000),
                            'status': 'error',
                            'error': 'Timeout checking shard',
                        }
        self.result['ms'] = int((time.time() - start_time) * 1000)
        return self.result


class StuckChunkHealth(Resource):
    """
        A continuing problem we see is that chunks will be successfully imported (chunk status changes to
        imported from importing) but the worker then hangs and never processes any more tasks. Attempts to
        get a useful stacktrace from stuck processes have so far been fruitless. There are two current working
        theories:

        1) There is a bug in the crate driver or crate server which causes the connection to hang after the
        import is finished. This is borne out somewhat by the issue seen where finished queries still show up
        in the sys.jobs table after they have completed. This may be fixed or mitigated by the latest versions
        of crate. (Current testing is with Crate v0.49.4)

        2) There is a bug in the celery setup somewhere. There are reports of use of redis with celery causing
        hangs but these are more about using it as a queueing backend and for older versions of celery. Monkey
        patches are being used which make sure that connections are returned to pools and that pools are
        closed (see redcelery package in requirements and at https://github.com/reversefold/redcelery) but the
        problem has persisted even with these patches in place.
    """
    def get(self):
        queues = QueueHealth().get()
        chunks = ChunkHealth().get()
        # TODO(jpatrin): This needs to be split per-shard when importer is refactored to have per-shard import queues
        import_queue_count = sum(count for queue, count in queues.items() if queue.endswith('.import_chunk'))
        importing_chunk_count = len([chunk for chunk in chunks if chunk['status'] == 'importing'])
        if importing_chunk_count == 0 and import_queue_count > 1:
            resp = {
                'status': 'error',
                'error': 'No chunks are importing but there are chunks waiting to import. '
                         'All import workers may be stuck. '
                         'Restart shinkansen ASAP to continue migrations.'
            }
        elif importing_chunk_count <= 1 and import_queue_count > 1:
            resp = {
                'status': 'warning',
                'warning': 'Some chunks are importing but there are more waiting to import. '
                'Some import workers appear to be stuck. '
                'Restart shinkansen soon to keep migrations flowing at a good pace.'
            }
        else:
            resp = {
                'status': 'ok',
            }
        resp['import_queue_count'] = import_queue_count
        resp['importing_chunk_count'] = importing_chunk_count
        return resp


def add_resource(api, resource, path):
    # We need to specify the endpoint here as the default is just the class name and the same class names are used in other versions
    api.add_resource(resource, path, endpoint=__name__ + '.' + resource.__name__)


def install_endpoints(api, ROOT_LINKS):
    ROOT_LINKS.append({
        'href': '/v5',
        'rel': 'v5',
        'method': 'GET',
    })
    add_resource(api, Root, '/v5')

    add_resource(api, Health, '/v5/health')
    add_resource(api, QueueHealth, '/v5/health/queues')
    add_resource(api, ChunkHealth, '/v5/health/chunks')
    add_resource(api, DatabaseHealth, '/v5/health/database')
    add_resource(api, StuckChunkHealth, '/v5/health/stuck')

    add_resource(api, Migration, '/v5/migration/<string:migration_id>')
    add_resource(api, MigrationTables, '/v5/migration/<string:migration_id>/tables')

    add_resource(api, Sources, '/v5/sources')

    add_resource(api, Source, '/v5/source/<string:source>')
    add_resource(api, SourceDestinations, '/v5/source/<string:source>/destinations')

    add_resource(api, SourceDestination, '/v5/source/<string:source>/destination/<string:destination>')
    add_resource(api, SourceDestinationFull, '/v5/source/<string:source>/destination/<string:destination>/full')
    add_resource(api, SourceDestinationLatest, '/v5/source/<string:source>/destination/<string:destination>/latest')
    add_resource(api, SourceDestinationDelta, '/v5/source/<string:source>/destination/<string:destination>/delta')

    add_resource(
        api, SourceDestinationDeltaAuto,
        '/v5/source/<string:source>/destination/<string:destination>/delta/auto')
    add_resource(api, SourceDestinationComplete, '/v5/source/<string:source>/destination/<string:destination>/complete')

    add_resource(
        api, SourceDestinationPartitions,
        '/v5/source/<string:source>/destination/<string:destination>/partitions')

    add_resource(
        api,
        SourceDestinationPartition,
        '/v5/source/<string:source>/destination/<string:destination>/partition/<int:partition_val>')

    add_resource(
        api,
        SourceDestinationPartitionLatest,
        '/v5/source/<string:source>/destination/<string:destination>/partition/<int:partition_val>/latest')

    add_resource(
        api,
        SourceDestinationPartitionFull,
        '/v5/source/<string:source>/destination/<string:destination>/partition/<int:partition_val>/full')

    add_resource(
        api,
        SourceDestinationPartitionDelta,
        '/v5/source/<string:source>/destination/<string:destination>/partition/<int:partition_val>/delta')

    add_resource(
        api, SourceDestinationPartitionDeltaAuto,
        '/v5/source/<string:source>/destination/<string:destination>/partition/<int:partition_val>/delta/auto')

    add_resource(
        api, SourceDestinationPartitionComplete,
        '/v5/source/<string:source>/destination/<string:destination>/partition/<int:partition_val>/complete')
