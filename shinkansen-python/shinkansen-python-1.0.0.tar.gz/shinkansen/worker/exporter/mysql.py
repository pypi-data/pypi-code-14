import copy
from datetime import datetime
import logging
import random
import subprocess
import time

from reversefold.util import ssh

from shinkansen import config, db, worker
from shinkansen.worker import (
    NULL_SENTINEL,
    BaseChunkWorker, CommandException, UnrecoverableError
)
from shinkansen.worker import streamer


log = logging.getLogger(__name__)


# populated at the end of this module
EXPORT_TASKS = {}


class ExportChunkWorkerMysql(BaseChunkWorker):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('log', log)
        super(ExportChunkWorkerMysql, self).__init__(*args, **kwargs)

    def _run(self):
        time.sleep(random.randint(0, 10))
        start = datetime.now()
        if self.c.source_type != 'mysql':
            raise UnrecoverableError('This exporter only supports mysql sources, passed in source_type was %r' % (
                self.c.source_type,))
        self.chunk.status = 'exporting'
        self.chunk.start_time = int(time.time() * 1000)
        self.chunk.update()
        source_host = config.SOURCES[self.c.source_shard]['config']['read_host']['host']
        with db.shard_connection(self.c.source_shard, read=True) as mysql_conn:
            self.log('Starting export')

            mysql_host_user = '%s@%s' % (
                config.SSH_USER, source_host)
            cmd = (
                'sudo mkdir -p %(source_dir)s && sudo chmod 777 %(source_dir)s; '
                '[ ! -e %(outfile)s ] || sudo rm %(outfile)s'
            ) % {
                'tmp_dir': config.TMP_DIR,
                'source_dir': worker.SOURCE_DIR,
                'outfile': self.c.export_filename,
            }
            sshcmd = (
                'ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -o LogLevel=ERROR '
                '-o ControlMaster=no -o ControlPath=none '
                '-p %r -i %s %s "%s"' % (
                    config.MYSQL_SSH_PORT, config.SSH_PRIVKEY, mysql_host_user, ssh.escape_double_quotes(cmd)))
            rm_existing = subprocess.Popen(
                sshcmd,
                shell=True,
                stdin=subprocess.PIPE)
            rm_existing.stdin.close()
            rm_existing.wait()
            if rm_existing.returncode != 0:
                raise CommandException('Checking for and removing export file failed with exit code %r' % (
                    rm_existing.returncode,))


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

            # We want to kick off the streamer here to enable streaming while the export file is still being written
            # but if we do and the export below fails the streamer will be stuck in an infinite loop and the next time
            # the export task gets retried we'll kick off yet another streamer task, potentially corrupting data.
            # TODO(jpatrin): A fix for this would be to use a random token so the streamer knows it belongs to the
            # running exporter. Before kicking off the streamer, write a file with a random UUID next to where the
            # exported file will be. Put the token in self.c so it gets passed to the streamer. When the streamer
            # starts up, read the token file and check it vs. the token in self.c. If it's different, mark the chunk
            # as failed, end the streamer without doing anything, and don't retry the task.
            #streamer.queue_stream_chunk(self.c)

            # TODO(jpatrin): Don't we need to add the join clause here to make the where_clauses work for inline
            # trimming?
            sql = (
                (
                    "SELECT %(columns)s INTO OUTFILE '%(outfile)s' CHARACTER SET utf8 "
                    # We use | as an escape character as MySQL's default of \ is problematic and at some times is not
                    # compatible with the csv module's parser.
                    """FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' ESCAPED BY '|' """
                    "LINES TERMINATED BY '\\n' "
                    "FROM %(schema)s.%(table)s %(table_alias)s WHERE %(wheres)s"
                    # Adding sorting here only slows down the query.
                    # "ORDER BY %(chunk_col)s ASC"
                ) % {
                    'columns': ', '.join(
                        (
                            # We're using NULL_SENTINEL here because MySQL uses a nonstandard value for null
                            # in its OUTFILE which is not as easy to detect and convert as I'd like.
                            "IF(%s IS NULL, '%s', %s)" % (
                                col.name,
                                NULL_SENTINEL,
                                mysql_conn.column_query_sql(col)
                            )
                        ) for col in self.c.export_columns
                    ),
                    'outfile': self.c.export_filename,
                    'schema': self.c.source_schema,
                    'table': self.c.table_config.table_name,
                    'table_alias': self.c.table_config.table_alias,
                    'wheres': ' AND '.join(wheres),
                }
            )
            with db.cursor(mysql_conn) as cur:
                cur.execute(sql % {'?': mysql_conn.PARAMETER_PLACEHOLDER}, where_values)
                self.c.num_records_exported = cur.rowcount

        # kick off the streamer
        streamer.queue_stream_chunk(self.c)

        self.chunk.num_records_exported = self.c.num_records_exported
        self.chunk.export_elapsed_ms = int((datetime.now() - start).total_seconds() * 1000)
        self.chunk.update()
        # The streaming may or may not have started, so we only update the status if it's still set to exporting
        self.chunk.update_status('exported', where_status='exporting')

        # signal to the processor that we have reached the end of the data
        self.log('Signaling EOF to conversion')
        cmd = 'sudo bash -c "echo STOP >> %s"' % (
            ssh.escape_double_quotes(self.c.export_filename),
        )
        signal_stop = subprocess.Popen(
            'ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -o LogLevel=ERROR '
            '-p %r -i %s %s@%s "%s"' % (
                config.MYSQL_SSH_PORT, config.SSH_PRIVKEY, config.SSH_USER,
                source_host,
                ssh.escape_double_quotes(cmd)),
            shell=True,
            stdin=subprocess.PIPE)
        signal_stop.stdin.close()
        signal_stop.wait()

        self.log('Finished chunk export num_records_exported=%s elapsed=%s',
                 self.c.num_records_exported, datetime.now() - start)
