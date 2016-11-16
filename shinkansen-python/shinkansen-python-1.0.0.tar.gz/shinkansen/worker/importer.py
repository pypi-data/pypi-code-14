from datetime import datetime
import logging
import subprocess
import time

from reversefold.util import ssh

from shinkansen import config, db
from shinkansen.worker import (
    NULL_SENTINEL,
    celery_app, import_queue, migration_task_wrapper,
    verifier,
    BaseChunkWorker, CommandException, Error
)


log = logging.getLogger(__name__)


class ImportChunkWorker(BaseChunkWorker):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('log', log)
        super(ImportChunkWorker, self).__init__(*args, **kwargs)

    def _import_to_crate(self):
        with db.shard_connection(self.c.destination_shard, read=True) as conn:
            self.log('Starting import')
            with db.cursor(conn) as cur:
                sql = "COPY %s.%s FROM '%s'" % (
                    self.c.destination_schema, self.c.table_config.table_name, self.c.import_filename)
                cur.execute(sql)
                self.c.num_records_imported = cur.rowcount
            conn.commit()

    def _import_to_mysql(self):
        with db.shard_connection(self.c.destination_shard, read=False) as conn:
            self.log('Starting import')
            with db.cursor(conn) as cur:
                sql = (
                    (
                        "LOAD DATA INFILE '%(infile)s' "
                        # TODO(jpatrin): If the mysql source had timestamp fields with the special value
                        # '0000-00-00 00:00:00' then the imports will fail if the mysql server is set to be strict about
                        # timestamp types. In this case adding IGNORE below will fix the issue, but may mask other
                        # issues. If this issue recurs we should probably add special support to the migrator to handle
                        # the special '0000-00-00 00:00:00' timestamp value, similar to what is done for NULL.
                        # "IGNORE "
                        "INTO TABLE %(schema)s.%(table)s CHARACTER SET utf8 "
                        # We use | as an escape character as MySQL's default of \ is problematic and at some times is
                        # not compatible with the csv module's parser.
                        """FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' ESCAPED BY '|' """
                        "LINES TERMINATED BY '\\n' "
                        '(%(columns)s) SET %(sets)s'
                    ) % {
                        'infile': self.c.import_filename,
                        'schema': self.c.destination_schema,
                        'table': self.c.table_config.table_name,
                        'columns': ', '.join(
                            ('' if col.ignore else '@') + col.name
                            for col in self.c.export_columns
                        ),
                        'sets': ', '.join(
                            "%s = IF(%s = '%s', NULL, %s)" % (
                                col.name,
                                '@' + col.name,
                                NULL_SENTINEL,
                                conn.column_insert_sql(col) % {'?': '@' + col.name}
                            )
                            for col in self.c.export_columns
                            if not col.ignore
                        ),
                    }
                )
                cur.execute(sql)
                self.c.num_records_imported = cur.rowcount
            conn.commit()

    def _run(self):
        if self.c.num_records_converted > 0:
            self.chunk.status = 'importing'
            self.chunk.update()
            start = datetime.now()
            if self.c.destination_type == 'crate':
                self._import_to_crate()
            elif self.c.destination_type == 'mysql':
                self._import_to_mysql()
            else:
                raise Error('Unknown destination type %r' % (self.c.destination_type,))

            self.log('Import to destination finished num_records_imported=%s destination_host=%s elapsed=%s',
                     self.c.num_records_imported, self.c.destination_host, datetime.now() - start)

            self.chunk.status = 'imported'
            self.chunk.num_records_imported = self.c.num_records_imported
            self.chunk.import_elapsed_ms = int((datetime.now() - start).total_seconds() * 1000)
            self.chunk.end_time = int(time.time() * 1000)
            self.chunk.update()
        else:
            self.log('No rows to import')
            self.chunk.status = 'empty'
            self.chunk.end_time = int(time.time() * 1000)
            self.chunk.update()

        if config.ENABLE_VERIFIER:
            verifier.queue_verification(self.c)

        # TODO(jpatrin): Refactor this into its own task so it can be independently retried
        try:
            cmd = (
                'ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -o LogLevel=ERROR '
                '-i %s -p %r %s@%s "sudo bash -c \'rm -f %s\'"' % (
                    config.SSH_PRIVKEY, self.c.destination_ssh_port, config.SSH_USER, self.c.destination_host,
                    ssh.escape_double_quotes(ssh.escape_single_quotes(self.c.import_filename))))
            rm_cmd = subprocess.Popen(
                cmd,
                shell=True,
                stdin=subprocess.PIPE)
            rm_cmd.stdin.close()
            rm_cmd.wait()
            if rm_cmd.returncode != 0:
                raise CommandException('Removing file on destination server failed with exit code %r' % (
                    rm_cmd.returncode,))
        except Exception, e:
            # We catch and log all exceptions here to make this task idempotent. We DO NOT want this task to be
            # retried at this point as duplicate imports can fail on mysql and would cause us to corrupt the crate
            # chunk import records.
            self.log('Exception during removal of destination file, removal will not be retried %r import_filename=%s',
                     e, self.c.import_filename)


if config.QUEUE_SYSTEM == 'multiprocessing':
    queue_import_chunk = import_queue.put
elif config.QUEUE_SYSTEM == 'celery':
    # TODO(jpatrin): Need import queues per-shard for mysql and crate
    # TODO(jpatrin): Once we split this queue, keep track of the queues, their names, and their shards
    # for use in the health API
    queue_import_chunk = celery_app.task(
        bind=True,
        name='shinkansen.worker.import_chunk'
    )(migration_task_wrapper(ImportChunkWorker)).delay
