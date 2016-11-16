import csv
import ctypes
from datetime import datetime
import logging
import multiprocessing
import json
import os
import socket
import subprocess
import sys
import time

import hdfs.client
from reversefold.util import chunked, multiproc, ssh, proc as proc_utils

import shinkansen
from shinkansen.worker import (
    stream_queue, archive_queue, celery_app, migration_task_wrapper, verifier,
    BaseChunkWorker, CommandException, Error,
    NULL_SENTINEL,
)
from shinkansen.worker import importer
from shinkansen import config, db


log = logging.getLogger(__name__)


# without this we'll get errors about field length
csv.field_size_limit(sys.maxsize)


CRATE_IDX = {
    cluster_name: multiprocessing.Value(ctypes.c_ulong, 0)
    for cluster_name in config.CRATE_SHARDS
}


class StreamChunkWorker(BaseChunkWorker):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('log', log)
        super(StreamChunkWorker, self).__init__(*args, **kwargs)
        self.start_convert = None

    def upsert(self, conn, records, _recursed=False):
        with db.cursor(conn) as cur:
            sql = (
                'INSERT INTO %(schema)s.%(table)s (%(columns)s) VALUES (%(placeholders)s) '
                'ON DUPLICATE KEY UPDATE %(sets)s'
            ) % {
                'schema': self.c.destination_schema,
                'table': self.c.table_config.table_name,
                'columns': ', '.join(col.name for col in self.c.export_columns),
                'placeholders': ', '.join(
                    conn.column_insert_sql(col) for col in self.c.export_columns
                ) % {'?': conn.PARAMETER_PLACEHOLDER},
                'sets': ', '.join(
                    '%s = VALUES(%s)' % (col.name, col.name)
                    for col in self.c.export_columns
                    if not col.is_primary_key
                ),
            }
            #self.log(sql.replace('%', '%%'))
            #self.log(repr(records).replace('%', '%%'))
            try:
                results = cur.executemany(sql, records)
            except Exception, e:
                if config.IGNORE_CONSTRAINT_FAILURES and 'foreign key constraint fails' in str(e) and not _recursed:
                    self.log('Foreign key constraint error, trying one by one')
                    for record in records:
                        try:
                            self.upsert(conn, [record], _recursed=True)
                        except Exception, e:
                            self.log('Record failed insert due to %r: %r', e, record)
                    return
                else:
                    raise
            num_rows = 0
            errors = []
            if results:
                for result in results:
                    if result['rowcount'] > -1:
                        num_rows += result['rowcount']
                    else:
                        self.log_error('Error upserting %r' % (result,))
                        errors.append(result)
            self.chunk.num_records_imported += num_rows
            self.chunk.update()
            self.log_debug('Upserted num_records=%r', num_rows)
            if errors:
                raise Error('Errors when upserting %r' % (errors,))
        conn.commit()

    @staticmethod
    def in_stream_generator(in_stream):
        for line in iter(in_stream.stdout.readline, b''):
            # We need to strip extra whitespace from the beginning and end of lines as mysql and crate may
            # add extra spaces that will confuse the parsers
            line = line.strip()
            if line == 'STOP':
                raise StopIteration
            yield line + '\n'

    def json_decoder_generator(self, line_generator):
        for line in line_generator:
            # We need to strip extra whitespace from the beginning and end of lines as mysql and crate may
            # add extra spaces that will confuse the parsers
            line = line.strip()
            try:
                yield json.loads(line)
            except Exception:
                self.log_error('Could not decode line %r', line)
                raise

    def row_generator(self, row_gen):
        for row in row_gen:
            if self.start_convert is None:
                self.start_convert = datetime.now()
                self.chunk.status = 'streaming'
                self.chunk.update()
            if len(row) != len(self.c.export_columns):
                self.log('Row does not have the correct number of columns %r', row)
                raise Error('row does not have the correct number of columns')
            self.c.num_records_converted += 1
            if self.c.num_records_converted % 1000 == 0:
                self.chunk.status = 'streaming'
                # NOTE: We're setting num_records_exported here as the crate exporter can't get a row count from crate
                self.chunk.num_records_exported = self.c.num_records_converted
                self.chunk.num_records_converted = self.c.num_records_converted
                self.chunk.update()
            yield row
            #yield {
            #    col.lname: col.type.coerce_func(val)
            #    for (col, val) in ((self.c.export_columns[i], row[i]) for i in xrange(len(row)))
            #}

    def _run_crate_any(self):
        start = datetime.now()
        self.log('Stream started')

        source_host = self.c.crate_data_node
        self.log('Streaming export directory export_dir=%s', self.c.export_dir)

        # TODO: use reversefold.util.ssh (can't currently due to its output munging)
        in_stream = subprocess.Popen(
            [
                'ssh',
                '-o', 'UserKnownHostsFile=/dev/null',
                '-o', 'StrictHostKeyChecking=no',
                '-o', 'LogLevel=ERROR',
                '-o', 'ControlMaster=no',
                '-o', 'ControlPath=none',
                '-t', '-t',
                '-C',
                '-p', str(source_host['ssh_port']),
                '-i', str(config.SSH_PRIVKEY),
                '%s@%s' % (config.SSH_USER, source_host['host']),
                """
                    EXPORT_DIR="%s"
                    while [ ! -e "${EXPORT_DIR}" ]; do
                        sleep 0.1
                    done
                    if ! ls "${EXPORT_DIR}"/*.json > /dev/null 2>&1; then
                        exit
                    fi
                    find "${EXPORT_DIR}" -type f -name "*.json" -print0 | xargs -0 sudo cat
                    exit
                """ % (ssh.escape_double_quotes(self.c.export_dir),)
            ],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE
        )
        if in_stream.poll() is not None:
            raise Error('starting stream from source failed')

        exc = False
        # Ensure that the process and its children are dead when this block exits.
        # This *may* allow the shell on the remote end to continue running, but at least our local
        # process will be shut down.
        with proc_utils.dead(in_stream, recursive=True):
            try:
                with db.shard_connection(self.c.destination_shard, read=False) as dest_conn:
                    self.start_convert = None
                    for chunk in chunked(
                        self.row_generator(
                            self.json_decoder_generator(
                                self.in_stream_generator(in_stream)
                            )
                        ),
                        config.PIPE_BULK_INSERT_SIZE
                    ):
                        self.upsert(dest_conn, chunk)

                self.chunk.num_records_converted = self.c.num_records_converted
                self.chunk.status = 'imported'
                if self.start_convert is not None:
                    self.chunk.convert_elapsed_ms = int((datetime.now() - self.start_convert).total_seconds() * 1000)
                self.chunk.update()

            except Exception:
                exc = True
                raise

            finally:
                # If we get an exception (or are interrupted) while the in_stream is open we need to make sure
                # it gets closed or we'll leave forever-running ssh processes and while loops on the remote server.
                # NOTE: This is not an issue for the out_stream as even if the worker is exiting the stdin pipe will
                # be closed by Python or the OS and the remote cat and local ssh process will naturally exit.
                self.log('Closing the in_stream')
                if in_stream.poll() is None:
                    try:
                        in_stream.stdin.write(chr(13))
                        in_stream.stdin.close()
                    except IOError:
                        pass
                start_wait_for_in_stream = time.time()
                while in_stream.poll() is None:
                    if time.time() - start_wait_for_in_stream > 2:
                        break
                    time.sleep(0.01)
                # The None case is handled in the finally below.
                # 130 is the code we get back if we send tail a Ctrl-C
                # 255 is the code we get back if we send the shell a Ctrl-C (i.e. when an exception brings us here
                # before the file exists)
                if in_stream.returncode != 0 and in_stream.returncode is not None:
                    #print(in_stream.stderr.read())
                    if exc:
                        self.log_error(
                            'Streaming file from source server failed with exit code %r',
                            in_stream.returncode)
                    else:
                        raise CommandException('Streaming file from source server failed with exit code %r' % (
                            in_stream.returncode,))

        # TODO(jpatrin): Refactor removal of the export_file into its own task so we can retry it as needed without
        # affecting the streamer tasks.
        # To make this task idempotent we handle exceptions here, errors below should not cause this task to be retried
        try:
            self.log('Removing the file from the source server export_dir=%s', self.c.export_dir)
            cmd = 'sudo bash -c "rm -r %s"' % (
                ssh.escape_double_quotes(self.c.export_dir),
            )
            ssh.SSHHost(
                source_host['host'], source_host['ssh_port'], config.SSH_USER,
                identity=config.SSH_PRIVKEY
            ).run(cmd)
        except Exception, e:
            self.log('Got exception while removing the source file, task will not be retried %r export_filename=%s',
                     e, self.c.export_filename)

        self.log('Done streaming chunk num_records_converted=%s elapsed=%s',
                 self.c.num_records_converted, datetime.now() - start)

        if config.ENABLE_VERIFIER:
            verifier.queue_verification(self.c)

    def set_destination_host(self):
        destination_shard_config = config.DESTINATIONS[self.c.destination_shard]

        if self.c.destination_type == 'crate':

            with CRATE_IDX[self.c.destination_shard].get_lock():
                data_nodes = destination_shard_config['config']['data_nodes']
                destination_node = data_nodes[CRATE_IDX[self.c.destination_shard].value]

                CRATE_IDX[self.c.destination_shard].value = (
                    (CRATE_IDX[self.c.destination_shard].value + 1) % len(data_nodes)
                )

            self.c.destination_host = destination_node['host']
            self.c.destination_ssh_port = destination_node['ssh_port']

        elif self.c.destination_type == 'mysql':
            self.c.destination_host = destination_shard_config['config']['write_host']['host']
            self.c.destination_ssh_port = destination_shard_config['config']['ssh_port']

        else:
            raise Error('Unknown destination type %r' % (self.c.destination_type,))

        self.chunk.destination_host = self.c.destination_host
        self.chunk.update()

    def _run(self):
        if self.c.source_type == 'mysql':
            return self._run_mysql_any()
        elif self.c.source_type == 'crate':
            return self._run_crate_any()
        else:
            raise shinkansen.UnrecoverableError(
                'Streaming combination not supported. source_type=%r destination_type=%r' % (
                    self.c.source_type, self.c.destination_type)
            )

    def _run_mysql_any(self):
        start = datetime.now()
        self.log('Stream started')

        source_host = config.SOURCES[self.c.source_shard]['config']['read_host']['host']

        self.log('Tailing export file export_filename=%s', self.c.export_filename)
        # TODO: use reversefold.util.ssh (can't currently due to its output munging)
        cmd = [
            'ssh',
            '-o', 'UserKnownHostsFile=/dev/null', '-o', 'StrictHostKeyChecking=no', '-o', 'LogLevel=ERROR',
            '-o', 'ControlMaster=no', '-o', 'ControlPath=none',
            '-C',
            '-p', str(config.MYSQL_SSH_PORT),
            '-t', '-t',
            '-i', str(config.SSH_PRIVKEY),
            '%s@%s' % (config.SSH_USER, source_host),
            # TODO: Do we even need the while here if we're not starting the streaming until after the export is done?
            """
                while [ ! -e "%(filename)s" ]; do
                    sleep 0.1;
                done
                sudo tail -f -c +0 "%(filename)s"
            """ % {
                'filename': ssh.escape_double_quotes(self.c.export_filename),
            }
        ]
        in_stream = subprocess.Popen(
            # Double -t forces a TTY, which allows us to send a Ctrl-C to the remote server below, which means
            # we won't leave any processes hanging.
            cmd,
            stdin=subprocess.PIPE, stdout=subprocess.PIPE)  # , stderr=sys.stderr.fileno())
        if in_stream.poll() is not None:
            raise Error('starting stream from source failed')

        # Ensure that the process and its children are dead when this block exits.
        # This *may* allow the shell on the remote end to continue running, but at least our local
        # process will be shut down.
        with proc_utils.dead(in_stream, recursive=True):
            try:
                self.set_destination_host()

                self.log('Writing import file to destination server import_filename=%s destination_host=%s',
                         self.c.import_filename, self.c.destination_host)
                cat_cmd = (
                    'sudo mkdir -p "%(tmp_dir)s/destination" && sudo chmod 777 "%(tmp_dir)s/destination" && '
                    # Remove before overwriting just in case we somehow have two streamers trying to write to the
                    # same file. Removing it makes sure we have our own inode.
                    'sudo bash -c \'rm -f "%(filename)s"; cat > "%(filename)s"\''
                ) % {
                    'tmp_dir': ssh.escape_double_quotes(config.TMP_DIR),
                    'filename': ssh.escape_single_quotes(
                        ssh.escape_double_quotes(
                            self.c.import_filename
                        )
                    ),
                }
                # TODO: use reversefold.util.ssh
                cmd = [
                    'ssh',
                    '-o', 'UserKnownHostsFile=/dev/null', '-o', 'StrictHostKeyChecking=no', '-o', 'LogLevel=ERROR',
                    '-o', 'ControlMaster=no', '-o', 'ControlPath=none',
                    '-C',
                    '-p', str(self.c.destination_ssh_port),
                    '-i', str(config.SSH_PRIVKEY),
                    '%s@%s' % (config.SSH_USER, self.c.destination_host),
                    cat_cmd
                ]
                out_stream = subprocess.Popen(
                    cmd,
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE)
                if out_stream.poll() is not None:
                    raise Error('starting stream to destination failed')

                with proc_utils.dead(out_stream, recursive=True):
                    (_, _, out_threads) = multiproc.run_subproc(
                        out_stream,
                        '[out_stream] ',
                        wait=False,
                        capture_output=False,
                        output_func=self.log_warning,
                        use_color=False)

                    start_convert = None
                    if not os.path.exists(config.TMP_DIR):
                        os.mkdir(config.TMP_DIR)
                    with open(self.c.backup_filename, 'w') as backup_file:
                        # TODO(jpatrin): Refactor to be more OO
                        if self.c.source_type == 'mysql' and self.c.destination_type == 'crate':
                            # NOTE(jpatrin): These values need to be the same as in the exporter for mysql
                            reader = csv.reader(
                                self.in_stream_generator(in_stream),
                                delimiter=',', quotechar='"', escapechar='|'
                            )
                            for row in reader:
                                if start_convert is None:
                                    start_convert = datetime.now()
                                    self.chunk.status = 'converting'
                                    self.chunk.update()
                                if len(row) != len(self.c.export_columns):
                                    self.log('Row does not have the correct number of columns %r', row)
                                    raise Error('row does not have the correct number of columns')
                                row_dict = {
                                    col.lname: (None if val == NULL_SENTINEL else col.type.coerce_func(val))
                                    for (col, val) in (
                                        (self.c.export_columns[i], val) for (i, val) in enumerate(row)
                                    )
                                }
                                json_string = json.dumps(row_dict)
                                out_stream.stdin.write(json_string)
                                out_stream.stdin.write('\n')
                                backup_file.write(json_string)
                                backup_file.write('\n')
                                self.c.num_records_converted += 1
                                if self.c.num_records_converted % 1000 == 0:
                                    self.chunk.status = 'converting'
                                    self.chunk.num_records_converted = self.c.num_records_converted
                                    self.chunk.update()
                        elif self.c.source_type == 'mysql' and self.c.destination_type == 'mysql':
                            for line in self.in_stream_generator(in_stream):
                                if start_convert is None:
                                    start_convert = datetime.now()
                                    self.chunk.status = 'converting'
                                    self.chunk.update()
                                out_stream.stdin.write(line)
                                backup_file.write(line)
                                # This counting may be flawed since we're not parsing the CSV, only counting lines
                                self.c.num_records_converted += 1
                                if self.c.num_records_converted % 1000 == 0:
                                    self.chunk.status = 'converting'
                                    self.chunk.num_records_converted = self.c.num_records_converted
                                    self.chunk.update()
                        else:
                            raise Error('Unsupported streaming combination source_type=%s destination_type=%s' % (
                                self.c.source_type, self.c.destination_type))

                    self.log('Closing the out_stream')
                    out_stream.stdin.close()
                    out_stream.wait()

                self.chunk.num_records_converted = self.c.num_records_converted
                self.chunk.status = 'converted'
                if start_convert is not None:
                    self.chunk.convert_elapsed_ms = int((datetime.now() - start_convert).total_seconds() * 1000)
                self.chunk.update()

            finally:
                # If we get an exception (or are interrupted) while the in_stream is open we need to make sure
                # it gets closed or we'll leave forever-running ssh processes and while loops on the remote server.
                self.log('Closing the in_stream')
                # send a Ctrl-C to the tail process
                try:
                    in_stream.stdin.write(chr(3))
                    in_stream.stdin.close()
                except IOError:
                    pass
                start_wait_for_in_stream = time.time()
                while in_stream.poll() is None:
                    if time.time() - start_wait_for_in_stream > 2:
                        break
                    time.sleep(0.01)
                # The None case is handled in the finally below.
                # 130 is the code we get back if we send tail a Ctrl-C
                # 255 is the code we get back if we send the shell a Ctrl-C (i.e. when an exception brings us here
                # before the file exists)
                if in_stream.returncode not in (None, 130, 255):
                    raise CommandException('Streaming file from source server failed with exit code %r' % (
                        in_stream.returncode,))

        if out_stream.returncode != 0:
            raise CommandException('Writing file to destination server failed with exit code %r' % (
                out_stream.returncode,))
        for thread in out_threads:
            thread.join()

        # kick off the import
        importer.queue_import_chunk(self.c)

        if self.c.num_records_converted == 0:
            self.log('Removing empty backup file backup_filename=%s', self.c.backup_filename)
            os.unlink(self.c.backup_filename)
        elif config.ENABLE_ARCHIVER:
            # kick off the archive
            queue_archive_chunk(self.c)

        # TODO(jpatrin): Refactor removal of the export_file into its own task so we can retry it as needed without
        # affecting the streamer tasks.
        # To make this task idempotent we handle exceptions here, errors below should not cause this task to be retried
        try:
            self.log('Removing the file from the source server export_filename=%s', self.c.export_filename)
            cmd = 'sudo bash -c "rm %s"' % (
                ssh.escape_double_quotes(self.c.export_filename),
            )
            rm_cmd = subprocess.Popen(
                'ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -o LogLevel=ERROR '
                '-o ControlMaster=no -o ControlPath=none '
                '-p %r -i %s %s@%s "%s"' % (
                    config.MYSQL_SSH_PORT, config.SSH_PRIVKEY, config.SSH_USER,
                    source_host,
                    ssh.escape_double_quotes(cmd)),
                shell=True,
                stdin=subprocess.PIPE)
            rm_cmd.stdin.close()
            rm_cmd.wait()
            if rm_cmd.returncode != 0:
                raise CommandException('Removing file on source server failed with exit code %r' % (
                    rm_cmd.returncode,))
        except Exception, e:
            self.log('Got exception while removing the source file, task will not be retried %r export_filename=%s',
                     e, self.c.export_filename)

        self.log('Done streaming chunk num_records_converted=%s elapsed=%s',
                 self.c.num_records_converted, datetime.now() - start)


class ArchiveChunkWorker(BaseChunkWorker):
    def _run(self):
        try:
            self.__run()
        except:
            # Don't allow the BaseChunkWorker to set the chunk's status to failed as it has already finished
            # migration at this point.
            self.chunk = None
            raise

    def __run(self):
        start = datetime.now()
        self.log('Archive started')

        if os.path.exists(self.c.backup_filename + '.gz'):
            os.unlink(self.c.backup_filename + '.gz')

        compress_start = datetime.now()
        self.log('Compressing local backup file backup_file=%s', self.c.backup_filename)
        compress_cmd = subprocess.Popen(
            ['gzip', self.c.backup_filename],
            stdin=subprocess.PIPE)
        compress_cmd.stdin.close()
        compress_cmd.wait()
        if compress_cmd.returncode != 0:
            raise CommandException('compressing failed with exit code %r' % (
                compress_cmd.returncode,))
        self.log('Compress finished backup_file=%s elapsed=%s', self.c.backup_filename, datetime.now() - compress_start)

        copy_start = datetime.now()
        compressed_filename = self.c.backup_filename + '.gz'
        self.log('Copying backup file to HDFS backup_file=%s', compressed_filename)
        client = hdfs.client.InsecureClient(config.HDFS_ENDPOINT, user=config.HDFS_USER, root=config.HDFS_PATH)

        dest_file = '%s/%s/%s/%u/%u/%u/%u/%u/%s' % (
            self.c.partition_val, self.c.source_schema, self.c.table_config.table_name,
            copy_start.year, copy_start.month, copy_start.day, copy_start.hour, copy_start.minute,
            os.path.basename(compressed_filename))
        client.upload(dest_file, compressed_filename, overwrite=True)
        self.log('Finished copying backup file to HDFS backup_file=%s elapsed=%s',
                 compressed_filename, datetime.now() - copy_start)

        self.log('Removing local file backup_file=%s', compressed_filename)
        os.unlink(compressed_filename)

        self.log('Done archiving chunk elapsed=%s', datetime.now() - start)


if config.QUEUE_SYSTEM == 'multiprocessing':
    queue_stream_chunk = stream_queue.put
    queue_archive_chunk = archive_queue.put
elif config.QUEUE_SYSTEM == 'celery':
    queue_stream_chunk = celery_app.task(
        bind=True,
        name='shinkansen.worker.stream_chunk'
    )(migration_task_wrapper(StreamChunkWorker)).delay
    queue_archive_chunk = celery_app.task(
        bind=True,
        name='shinkansen.worker.archive_chunk_%s' % (socket.gethostname(),)
    )(migration_task_wrapper(ArchiveChunkWorker)).delay
