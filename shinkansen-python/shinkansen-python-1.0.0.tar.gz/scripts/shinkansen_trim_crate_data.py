#!/usr/bin/env python
"""
Usage:
    trim_crate_data.py [--delete]

Options:
    -h --help    This help text
    -d --delete  Run the delete queries
"""
from __future__ import print_function
import datetime

import docopt

from shinkansen import config, db


def get_count(conn, sql):
    with db.cursor(conn) as cur:
        cur.execute('SELECT COUNT(*) ' + sql)
        (num_rows,) = cur.fetchone()
    return num_rows


def trim_table(conn, shard_config, table_config, delete, partition_val=None, partition_trimming_threshold=None):
    if partition_val is None or partition_trimming_threshold is None:
        trim_timedelta = table_config.trim_timedelta
    else:
        trim_timedelta = partition_trimming_threshold
        if (
            trim_timedelta is not None
            and table_config.trim_timedelta is not None
            and table_config.trim_timedelta <= trim_timedelta
        ):
            print('Global table trimming for %s more agressive than partition %s' % (
                table_config.table_name, partition_val
            ))
            return
    if trim_timedelta is None:
        print('No trimming timedelta for table %s' % (table_config.table_name,))
        return
    trim_time = datetime.datetime.now() - trim_timedelta
    trim_time_str = trim_time.strftime('%Y-%m-%dT%H:%M:%S')
    sql = "FROM %s.%s WHERE %s < '%s'" % (
        shard_config['default_schema_name'], table_config.table_name, table_config.trim_column,
        trim_time_str)
    if partition_val is not None:
        sql += ' AND %s = %u' % (table_config.partition_col, partition_val)
    trim_data(conn, sql, trim_time_str, shard_config, table_config.table_name, delete, partition_val)


def trim_data(conn, sql, trim_time_str, shard_config, table_name, delete, partition_val):
    num_rows = get_count(conn, sql)
    if delete:
        print('Deleting %r from %s.%s older than %s%s' % (
            num_rows, shard_config['default_schema_name'], table_name, trim_time_str,
            '' if partition_val is None else ' for partition %s' % (partition_val,)
        ))
        with db.cursor(conn) as cur:
            cur.execute('DELETE ' + sql)
    else:
        print('%r records to delete from %s.%s older than %s%s' % (
            num_rows, shard_config['default_schema_name'], table_name, trim_time_str,
            '' if partition_val is None else ' for partition %s' % (partition_val,)
        ))


def trim_shard(conn, shard_name, shard_config, delete, partition_val=None, partition_trimming_threshold=None):
    print('Processing shard %s%s' % (
        shard_name,
        '' if partition_val is None else ' for partition %s' % (partition_val,)
    ))
    for table_config in shard_config['tables']:
        if table_config.trim_column is None:
            print('No trim column for table %s' % (table_config.table_name,))
            continue
        trim_table(conn, shard_config, table_config, delete, partition_val, partition_trimming_threshold)
    print()


def main():
    args = docopt.docopt(__doc__)
    for shard_name, shard_config in config.CRATE_SHARDS.items():
        with db.shard_connection(shard_name, read=False) as conn:
            trim_shard(conn, shard_name, shard_config, args['--delete'])
    for partition_val, partition_trimming_threshold in config.PARTITION_SPECIFIC_TRIMMING_THRESHOLDS.items():
        for shard_name, shard_config in config.CRATE_SHARDS.items():
            if isinstance(partition_trimming_threshold, datetime.timedelta):
                shard_partition_trimming_threshold = partition_trimming_threshold
            else:
                shard_partition_trimming_config = partition_trimming_threshold.get(shard_config['shard_type'])
                if shard_partition_trimming_config is None:
                    continue
                if (
                    'shard_names' in shard_partition_trimming_config
                    and shard_name not in shard_partition_trimming_config['shard_names']
                ):
                    continue
                shard_partition_trimming_threshold = shard_partition_trimming_config['threshold']
            with db.shard_connection(shard_name, read=False) as conn:
                trim_shard(
                    conn, shard_name, shard_config, args['--delete'], partition_val, shard_partition_trimming_threshold)

if __name__ == '__main__':
    main()
