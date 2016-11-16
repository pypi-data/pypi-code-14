from collections import OrderedDict
import logging

import mox

from shinkansen import config, data, orm, worker
from shinkansen.worker import streamer


class TestableStreamChunkWorker(streamer.StreamChunkWorker):
    def __init__(self, chunk_config, chunk):
        # we don't want to test BaseChunkWorker.__init__ here so override it
        self.c = chunk_config
        self.redis_conn = None
        self.chunk = chunk
        self.logger = logging.getLogger(__name__)


class TestStreamer(mox.MoxTestBase):
    def setUp(self):
        super(TestStreamer, self).setUp()

        # Keep these in order so the tests, which rely on ordering, don't fail
        config.SHARD_SUFFIXES = OrderedDict([
            ('daily', ''),
            ('weekly', '_w'),
            ('monthly', '_m'),
        ])
        config.MYSQL_SHARDS = {
            'shn': {
                'tables': [
                    ('TableA', 'filter_col_a', 'chunk_col_a'),
                    ('TableB', 'filter_col_b', 'chunk_col_b'),
                ],
                'default_schema_name': 'mysql',
                'read_host': {'host': 'mysql_read'},
                'write_host': {'host': 'mysql_write'},
                'ssh_port': 2442,
            },
        }
        config.CRATE_SHARDS = {
        }
        config.SOURCES = {
            'shn': {'type': 'mysql', 'config': config.MYSQL_SHARDS['shn']},
        }
        config.DESTINATIONS = {
            'shn': {'type': 'mysql', 'config': config.MYSQL_SHARDS['shn']},
            'crate': {'type': 'crate', 'config': {'data_nodes': [
                {'host': 'crate0', 'ssh_port': 12}, {'host': 'crate1', 'ssh_port': 35}]}}
        }
        self.chunk = self.mox.CreateMock(orm.Chunk)

    def context(self, val=None):
        ctx = self.mox.CreateMockAnything()
        ctx.__enter__().AndReturn(val)
        ctx.__exit__(mox.IgnoreArg(), mox.IgnoreArg(), mox.IgnoreArg())
        return ctx

    def test_set_destination_host_mysql(self):
        self.c = worker.ChunkConfig(
            'mid', data.TableConfig('table', 'tcol', 'ccol', None), [], 1, 'ns', 'shn', 'shn', 1, 1, 1)
        self.chunk.update()

        self.mox.ReplayAll()
        stream_worker = TestableStreamChunkWorker(self.c, self.chunk)
        stream_worker.set_destination_host()
        self.assertEqual(self.c.destination_host, 'mysql_write')
        self.assertEqual(self.c.destination_ssh_port, 2442)
        self.assertEqual(self.chunk.destination_host, 'mysql_write')

    def test_set_destination_host_crate(self):
        streamer.CRATE_IDX['crate'] = self.mox.CreateMockAnything()
        streamer.CRATE_IDX['crate'].value = 1
        streamer.CRATE_IDX['crate'].get_lock().AndReturn(self.context())
        self.c = worker.ChunkConfig(
            'mid', data.TableConfig('table', 'tcol', 'ccol', None), [], 1, 'ns', 'shn', 'crate', 1, 1, 1)
        self.chunk.update()

        self.mox.ReplayAll()
        stream_worker = TestableStreamChunkWorker(self.c, self.chunk)
        stream_worker.set_destination_host()
        self.assertEqual(self.c.destination_host, 'crate1')
        self.assertEqual(self.chunk.destination_host, 'crate1')
        self.assertEqual(self.c.destination_ssh_port, 35)
        self.assertEqual(streamer.CRATE_IDX['crate'].value, 0)
