import copy
from datetime import datetime
import logging
import os
import random
import threading
import time

from reversefold.util import ssh

from shinkansen import config, db, worker
from shinkansen.worker import (
    BaseChunkWorker, CommandException, UnrecoverableError
)
from shinkansen.worker import streamer


log = logging.getLogger(__name__)


# populated at the end of this module
EXPORT_TASKS = {}


class ExportChunkWorkerCrate(BaseChunkWorker):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('log', log)
        super(ExportChunkWorkerCrate, self).__init__(*args, **kwargs)

    def _run(self):
        time.sleep(random.randint(0, 10))
        start = datetime.now()
        if self.c.source_type != 'crate':
            raise UnrecoverableError('This exporter only supports crate sources, passed in source_type was %r' % (
                self.c.source_type,))
        self.chunk.status = 'exporting'
        self.chunk.start_time = int(time.time() * 1000)
        self.chunk.update()
        with db.shard_connection(self.c.source_shard, read=True) as crate_conn:
            self.log('Starting export')

            self.c.export_dir = os.path.join(worker.SOURCE_DIR, ('%s_%s.%s_%s_%s' % (
                self.c.migration_id, self.c.source_schema, self.c.table_config.table_name, self.c.partition_val,
                self.c.chunk_num)))

            def make_source_dir(node):
                cmd = (
                    'sudo mkdir -p %(export_dir)s && sudo chmod 777 %(export_dir)s'
                ) % {
                    'export_dir': self.c.export_dir,
                }
                try:
                    ssh.SSHHost(
                        node['host'], node['ssh_port'], config.SSH_USER,
                        identity=config.SSH_PRIVKEY
                    ).run(cmd)
                except ssh.SSHException, e:
                    raise CommandException('Checking for and removing export file failed %r' % (e,))

            crate_cluster = config.DESTINATIONS[self.c.source_shard]
            data_nodes = crate_cluster['config']['data_nodes']
            threads = []
            for node in data_nodes:
                thread = threading.Thread(target=make_source_dir, args=(node,))
                thread.start()
                threads.append(thread)
            for thread in threads:
                thread.join()

            # Inline trimming may be in self.c.where_clauses
            wheres = copy.deepcopy(self.c.where_clauses)
            where_values = copy.deepcopy(self.c.where_values)
            wheres.extend([
                '%s >= %%(?)s' % (self.c.table_config.chunk_col,),
                '%s < %%(?)s' % (self.c.table_config.chunk_col,),
            ])
            where_values.extend([
                self.c.start_id,
                self.c.start_id + self.c.chunk_size,
            ])

            if self.c.table_config.join:
                # TODO: This is a HORRIBLE HACK that removes the hard-coded table alias from the partition and chunk
                # columns.
                # It is likely to cause problems. A refactoring of the join code is needed.
                column_alias = '%s.' % (self.c.table_config.table_alias,)
                fixed_wheres = []
                for where in wheres:
                    if where.startswith(column_alias):
                        where = where[len(column_alias):]
                    fixed_wheres.append(where)
                wheres = fixed_wheres

            # We want to kick off the streamer here to enable streaming while the export file is still being written
            # but if we do and the export below fails the streamer will be stuck in an infinite loop and the next time
            # the export task gets retried we'll kick off yet another streamer task, potentially corrupting data.
            # TODO(jpatrin): A fix for this would be to use a random token so the streamer knows it belongs to the
            # running exporter. Before kicking off the streamer, write a file with a random UUID next to where the
            # exported file will be. Put the token in self.c so it gets passed to the streamer. When the streamer
            # starts up, read the token file and check it vs. the token in self.c. If it's different, mark the chunk
            # as failed, end the streamer without doing anything, and don't retry the task.
            # NOTE: This would only work with crate if we append the STOP sentinel to all of the json files that each
            # node writes to export_dir or if we come up with another way to know when the export is finished.
            #streamer.queue_stream_chunk(self.c)

            # TODO(jpatrin): Don't we need to add the join clause here to make the where_clauses work for inline
            # trimming? They won't work with COPY TO, but we may need to figure out a way to support it.
            sql = (
                "COPY %(schema)s.%(table)s (%(columns)s) "
                "WHERE %(wheres)s "
                "TO DIRECTORY '%(export_dir)s' "
                "WITH (format='json_array') "
            ) % {
                'columns': ', '.join(col.name for col in self.c.export_columns),
                'schema': self.c.source_schema,
                'table': self.c.table_config.table_name,
                'wheres': ' AND '.join(wheres),
                'export_dir': self.c.export_dir,
            }
            #self.log_warning('%s', sql)
            #self.log_warning(repr(where_values))
            with db.cursor(crate_conn) as cur:
                cur.execute(sql % {'?': crate_conn.PARAMETER_PLACEHOLDER}, where_values)
                self.c.num_records_exported = cur.rowcount

        chunk_copy = None
        i = 0
        # kick off the streamers
        for node in data_nodes:
            # TODO: we're kicking off a streamer per node, which means we have multiple streamers running per chunk
            # This means they all update the same chunk record, making the system think the chunk is finished importing
            # when the first streamer finishes. This makes the migration verify before it should and may cause parallel
            # migrations when we don't want them.

            if chunk_copy is None:
                chunk_copy = self.chunk.copy()
                self.chunk.delete()
                self.chunk = None
            chunk = chunk_copy.copy()
            if self.chunk is None:
                self.chunk = chunk
            else:
                chunk.status = 'exported'
            chunk.num_records_exported = 0
            chunk.num_records_converted = 0
            chunk.num_records_imported = 0
            chunk.chunk_num = str(chunk.chunk_num) + ':' + str(i)
            chunk.insert()

            node_config = copy.deepcopy(self.c)
            node_config.chunk_num = chunk.chunk_num
            node_config.crate_data_node = node
            streamer.queue_stream_chunk(node_config)

            i += 1

        self.chunk.num_records_exported = self.c.num_records_exported
        self.chunk.export_elapsed_ms = int((datetime.now() - start).total_seconds() * 1000)
        self.chunk.update()
        # The streaming may or may not have started, so we only update the status if it's still set to exporting
        self.chunk.update_status('exported', where_status='exporting')

        # NOTE: This won't work with crate unless we change it to do it to all json files in the export_dir. For now
        # with the streamer being started after the export is finished the STOP sentinel isn't needed.
        # # signal to the processor that we have reached the end of the data
        # self.log('Signaling EOF to conversion')
        # cmd = 'sudo bash -c "echo STOP >> %s"' % (
        #     ssh.escape_double_quotes(self.c.export_filename),
        # )
        # signal_stop = subprocess.Popen(
        #     'ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -o LogLevel=ERROR '
        #     '-p %r -i %s %s@%s "%s"' % (
        #         config.CRATE_SSH_PORT, config.SSH_PRIVKEY, config.SSH_USER,
        #         source_host,
        #         ssh.escape_double_quotes(cmd)),
        #     shell=True,
        #     stdin=subprocess.PIPE)
        # signal_stop.stdin.close()
        # signal_stop.wait()

        self.log('Finished chunk export num_records_exported=%s elapsed=%s',
                 self.c.num_records_exported, datetime.now() - start)
