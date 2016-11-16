from __future__ import print_function
from copy import deepcopy
import socket
import sys

from .defaults import *
try:
    from config_local import *
except ImportError:
    print('config_local not found, using defaults', file=sys.stderr)


if MYSQL_SHARD_TABLES is None:
    MYSQL_SHARD_TABLES = SHARD_TABLES
if CRATE_SHARD_TABLES is None:
    CRATE_SHARD_TABLES = SHARD_TABLES


# Convert legacy config (host and port in top-level host config) into read_host
# and write_host if they are not also present.
for host in MYSQL_HOSTS.values():
    if 'host' in host:
        host.setdefault('port', 3306)
        host_entry = {
            'host': host['host'],
            'port': host['port'],
            'host_type': host.get('host_type', 'managed'),
        }
        if 'read_host' not in host:
            host['read_host'] = host_entry
        if 'write_host' not in host:
            host['write_host'] = host_entry
        del host['host']
        del host['port']
    if 'shards' not in host:
        host['shards'] = SHARD_SUFFIXES.keys()


if len(MYSQL_SHARDS) == 0:
    # MYSQL_SHARDS is used to know where data lives
    for _key, _data in MYSQL_HOSTS.items():
        for _shard in _data['shards']:
            _shard_data = {
                'default_schema_name': _data['schema_base_name'] + SHARD_SUFFIXES[_shard],
                'tables': MYSQL_SHARD_TABLES[_shard],
                'ssh_port': MYSQL_SSH_PORT,
                'queue_key': _key,
            }

            # Set up the full connect keyword args for both the read_host and write_host
            for _type in ['read_host', 'write_host']:
                if _type not in _data:
                    continue
                _host_params = {
                    'host': _data[_type]['host'],
                    'port': _data[_type]['port'],
                    'user': _data['user'],
                    'passwd': _data['passwd'],
                    'db': _shard_data['default_schema_name'],
                }
                _shard_data[_type] = _host_params

            MYSQL_SHARDS[_key + SHARD_SUFFIXES[_shard]] = _shard_data


for _, _crate_cluster_config in CRATE_CLUSTERS.items():
    _crate_cluster_config.setdefault('data_nodes', _crate_cluster_config['client_nodes'])
    if 'shards' not in _crate_cluster_config:
        _crate_cluster_config['shards'] = SHARD_SUFFIXES.keys()


if len(CRATE_SHARDS) == 0:
    for _name, _data in CRATE_CLUSTERS.items():
        _all_shard_config = _data.get('shard_config', {})
        for _shard in _data['shards']:
            _suffix = SHARD_SUFFIXES[_shard]
            _shard_config = _all_shard_config.get(_shard, {})
            if 'tables' in _shard_config:
                _tables = []
                for _table_config in CRATE_SHARD_TABLES[_shard]:
                    if _table_config.table_name in _shard_config['tables']:
                        _tables.append(_table_config)
            else:
                _tables = CRATE_SHARD_TABLES[_shard]
            if _shard_config.get('notrim', False):
                # Make a copy of all of the TableConfig entries so we change the trim attributes
                # only for this shard.
                _tables = deepcopy(_tables)
                for _table_config in _tables:
                    _table_config.trim_timedelta = None
            CRATE_SHARDS[_name + _suffix] = {
                'shard_type': _shard,
                'client_nodes': _data['client_nodes'],
                'data_nodes': _data['data_nodes'],
                'default_schema_name': 'shn' + _suffix if _suffix else _data['default_schema'],
                'tables': _tables,
                'queue_key': _name,
            }


# If we get straight strings as crate hosts, make it a dict
for _name, _cluster_config in CRATE_SHARDS.items():
    for _type in ['client_nodes', 'data_nodes']:
        _nodes = []
        for _node in _cluster_config[_type]:
            if isinstance(_node, basestring):
                _node = {
                    'host': _node,
                    'http_port': CRATE_HTTP_PORT,
                    'tcp_port': CRATE_TCP_PORT,
                    'ssh_port': CRATE_SSH_PORT,
                }
            _nodes.append(_node)
        _cluster_config[_type] = _nodes


# If no sources have been specifically defined, support all mysql and crate shards as sources
if len(SOURCES) == 0:
    for _shard, _data in MYSQL_SHARDS.items():
        if 'read_host' in _data:
            SOURCES[_shard] = {'type': 'mysql'}
    for _shard in CRATE_SHARDS:
        SOURCES[_shard] = {'type': 'crate'}


# If no destinations have been specifically defined, support all mysql and crate shards as destinations
if len(DESTINATIONS) == 0:
    for _shard, _data in MYSQL_SHARDS.items():
        if 'write_host' in _data:
            DESTINATIONS[_shard] = {'type': 'mysql'}
    for _shard in CRATE_SHARDS:
        DESTINATIONS[_shard] = {'type': 'crate'}


# SOURCES and DESTINATIONS, before this point, are just stubs pointing to shards.
# Point the config keys to the full config.
for _dict in [SOURCES, DESTINATIONS]:
    for _key, _data in _dict.items():
        if _data['type'] == 'mysql':
            _data['config'] = MYSQL_SHARDS[_key]
        elif _data['type'] == 'crate':
            _data['config'] = CRATE_SHARDS[_key]
        else:
            raise Exception('Data type unknown: %r' % (_data['type'],))


# CELERY settings, not meant to be externally configured
CELERY_RESULT_DB_SHORT_LIVED_SESSIONS = True
CELERY_ACKS_LATE = True
CELERYD_PREFETCH_MULTIPLIER = 1
CELERY_ANNOTATIONS = {
    '*': {
        'acks_late': True,
        'default_retry_delay': 30,
        'max_retries': None,
        'track_started': True,
    }
}
CELERY_ACCEPT_CONTENT = ['pickle']
CELERY_HIJACK_ROOT_LOGGER = False

CELERY_ROUTES = {}

for _shard_config in DESTINATIONS.values():
    for _taskname in ['shinkansen.worker.verify_%s']:
        _taskname = _taskname % (_shard_config['config']['queue_key'])
        CELERY_ROUTES[_taskname] = {'queue': _taskname}

for _shard_config in SOURCES.values():
    for _taskname in [
        'shinkansen.worker.start_migration_%s',
        'shinkansen.worker.export_chunk_%s',
        'shinkansen.worker.pipe_%s',
    ]:
        _taskname = _taskname % (_shard_config['config']['queue_key'])
        CELERY_ROUTES[_taskname] = {'queue': _taskname}

for _taskname in [
    'shinkansen.worker.stream_chunk',
    # The archive queue is always specific to the host since the files are on the local filesystem
    'shinkansen.worker.archive_chunk_%s' % (socket.gethostname(),),
    'shinkansen.worker.import_chunk',
]:
    CELERY_ROUTES[_taskname] = {
        'queue': _taskname,
    }
