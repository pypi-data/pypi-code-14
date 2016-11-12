import os
import os.path
import shutil
import tempfile
from unittest import TestCase

from . import smart_pipe


class TestSmartPipeWriter(TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_basic(self):
        path = os.path.join(self.test_dir, "test1")
        writer = smart_pipe.SmartPipeWriter(path)

        writer.checkpoint(b'\x00')
        writer.append(b'\x00:v1', b'test')
        writer.append(b'\x00:v2', b't2')
        writer.checkpoint(b'\x01')
        writer.append(b'\x01:v1', b't3')
        writer.close()

        data_expected = \
            bytearray([4, 0, 0, 0]) + \
            b'\x00:v1' + \
            bytearray([4, 0, 0, 0]) + \
            b'test' + \
            bytearray([4, 0, 0, 0]) + \
            b'\x00:v2' + \
            bytearray([2, 0, 0, 0]) + \
            b't2' + \
            bytearray([4, 0, 0, 0]) + \
            b'\x01:v1' + \
            bytearray([2, 0, 0, 0]) + \
            b't3'

        with open(path + smart_pipe.SmartPipeWriter.DATA_EXT, 'rb') as fd:
            data = fd.read()
            self.assertEqual(data, data_expected)

        index_expected =  bytearray([
            1, 0, 0, 0,
            0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            1, 0, 0, 0,
            1,
            30, 0, 0, 0, 0, 0, 0, 0,
            30, 0, 0, 0, 0, 0, 0, 0,
        ])

        with open(path + smart_pipe.SmartPipeWriter.INDEX_EXT, 'rb') as fd:
            data = fd.read()
            self.assertEqual(data, index_expected)


class TestIndexWriter(TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_basic(self):
        path = os.path.join(self.test_dir, "test1.idx")
        writer = smart_pipe.IndexWriter(path)

        writer.append(b'1', 0, 0)
        writer.append(b'2', 10, 10)
        writer.close()

        with open(path, "rb") as fd:
            data = fd.read()
            expected = bytearray([1, 0, 0, 0,                 # len of the key
                                  ord('1'),                   # key
                                  0, 0, 0, 0, 0, 0, 0, 0,     # offset1
                                  0, 0, 0, 0, 0, 0, 0, 0,     # offset2
                                  1, 0, 0, 0,                 # len of the key
                                  ord('2'),                   # key
                                  10, 0, 0, 0, 0, 0, 0, 0,    # offset1
                                  10, 0, 0, 0, 0, 0, 0, 0,    # offset2
                                  ])
            self.assertEqual(data, expected)


class TestIndexReader(TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_basic(self):
        path = os.path.join(self.test_dir, "test_writer_idx")
        writer = smart_pipe.IndexWriter(path)
        writer.append(b'1', 0, 0)
        writer.append(b'2', 10, 15)
        writer.append(b'3', 15, 20)
        writer.close()

        reader = smart_pipe.IndexReader(path)
        self.assertEqual([b'1', b'2', b'3'], reader.keys)
        self.assertEqual({b'1': (0, 0), b'2': (10, 15), b'3': (15, 20)}, reader.ofs_map)


class TestSmartPipeWriter(TestCase):
    uncomp_prefix = "data1"
    comp_prefix = "data2"

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def _create_data(self, prefix, compress):
        writer = smart_pipe.SmartPipeWriter(prefix, compress=compress)
        writer.checkpoint(b'1')
        writer.append(b'k1', b'v1')
        writer.append(b'k2', b'v2')
        writer.checkpoint(b'2')
        writer.append(b'k3', b'v3')
        writer.close()

    def _test_data(self, prefix):
        reader = smart_pipe.SmartPipeReader(prefix)
        self.assertEqual(b'1', reader.get_next_block_key())

        expected = [(b'k1', b'v1'), (b'k2', b'v2')]

        self.assertEqual((24, 24), reader._get_block_sizes())

        for idx, (k, v) in enumerate(reader.pull_block()):
            self.assertEqual(k, expected[idx][0])
            self.assertEqual(v, expected[idx][1])

        self.assertEqual(b'2', reader.get_next_block_key())
        expected = [(b'k3', b'v3')]
        for idx, (k, v) in enumerate(reader.pull_block()):
            self.assertEqual(k, expected[idx][0])
            self.assertEqual(v, expected[idx][1])
        self.assertIsNone(reader.get_next_block_key())

    def test_uncompressed(self):
        path = os.path.join(self.test_dir, "uncomp")
        self._create_data(path, compress=False)
        self._test_data(path)

    def test_compressed(self):
        path = os.path.join(self.test_dir, "comp")
        self._create_data(path, compress=True)
        self._test_data(path)


class TestSmartPipeReader(TestCase):
    test_dir = None

    @staticmethod
    def setUpClass():
        test_dir = tempfile.mkdtemp()
        TestSmartPipeReader._make_data(os.path.join(test_dir, "uncomp"), False)
        TestSmartPipeReader._make_data(os.path.join(test_dir, "comp"), True)
        TestSmartPipeReader.test_dir = test_dir

    @staticmethod
    def tearDownClass():
        shutil.rmtree(TestSmartPipeReader.test_dir)

    @staticmethod
    def _make_data(prefix, compress):
        writer = smart_pipe.SmartPipeWriter(prefix, compress=compress)
        writer.checkpoint(b'1')
        writer.append(b'k1', b'v1')
        writer.append(b'k2', b'v2')
        writer.checkpoint(b'2')
        writer.append(b'k3', b'v3')
        writer.checkpoint(b'3')
        writer.append(b'k4', b'v4')
        writer.close()

    def _read_data(self, reader):
        data = []
        while True:
            c_key = reader.get_next_block_key()
            if c_key is None:
                break
            data.append(c_key)
            for k, v in reader.pull_block():
                data.append((k, v))
        return data

    def _peek_block(self, reader, key):
        data = []
        for k, v in reader.pull_block(key):
            data.append((k, v))
        return data

    def test_linear(self):
        expected = [b'1', (b'k1', b'v1'), (b'k2', b'v2'), b'2', (b'k3', b'v3'), b'3', (b'k4', b'v4')]

        reader = smart_pipe.SmartPipeReader(os.path.join(self.test_dir, "uncomp"))
        data = self._read_data(reader)
        self.assertEqual(data, expected)

        reader = smart_pipe.SmartPipeReader(os.path.join(self.test_dir, "comp"))
        data = self._read_data(reader)
        self.assertEqual(data, expected)

    def test_middle_read_uncomp(self):
        reader = smart_pipe.SmartPipeReader(os.path.join(self.test_dir, "uncomp"))
        data = self._peek_block(reader, b'2')
        self.assertEqual(data, [(b'k3', b'v3')])

    def test_middle_read_comp(self):
        reader = smart_pipe.SmartPipeReader(os.path.join(self.test_dir, "comp"))
        data = self._peek_block(reader, b'2')
        self.assertEqual(data, [(b'k3', b'v3')])

    # def test_simple(self):
    #     comp = zlib.compressobj()
    #     r = comp.compress(b'123456789')
    #     r += comp.flush(zlib.Z_FULL_FLUSH)
    #
    #     v = comp.compress(b'123456789')
    #     v += comp.flush(zlib.Z_FULL_FLUSH)
    #     dec_obj = zlib.decompressobj(-15, zdict=b'')
    #     res = dec_obj.decompress(v)
    #     data = b'\x62\x62\x60\x60\xC8\x36\x62\x02\x92\x65\x46\x00\x00\x00\x00\xFF\xFF'
    #     res = zlib.decompress(data, -15)
    #     print(res)

    def test_large_data(self):
        writer = smart_pipe.SmartPipeWriter(os.path.join(self.test_dir, "large"), compress=True)
        writer.checkpoint(b'1')
        for _ in range(1024):
            writer.append(b'k1', os.urandom(256))
        writer.checkpoint(b'2')
        writer.append(b'k2', b'v2')
        writer.close()

        reader = smart_pipe.SmartPipeReader(os.path.join(self.test_dir, "large"))
        for k, v in reader.pull_block(b'2'):
            self.assertEqual(k, b'k2')
            self.assertEqual(v, b'v2')

    def test_multiple_seeks(self):
        path = os.path.join(self.test_dir, "multiple")
        writer = smart_pipe.SmartPipeWriter(path, compress=True)
        writer.checkpoint(b'1')
        writer.append(b'a', b'c')
        writer.append(b'b', b'c')
        writer.checkpoint(b'2')
        writer.append(b'b', b'c')
        writer.checkpoint(b'3')
        writer.append(b'a', b'c')
        writer.close()

        reader = smart_pipe.SmartPipeReader(path)
        for k, v in reader.pull_block(b'3'):
            self.assertEqual(k, b'a')
            self.assertEqual(v, b'c')
        for k, v in reader.pull_block(b'2'):
            self.assertEqual(k, b'b')
            self.assertEqual(v, b'c')
