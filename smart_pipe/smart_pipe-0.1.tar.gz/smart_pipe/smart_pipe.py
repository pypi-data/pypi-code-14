"""
Smart pipe storage scheme
"""
import os

import struct
import zlib


def _detect_data_path(prefix):
    # try uncompressed
    base = prefix + SmartPipeWriter.DATA_EXT
    if os.path.exists(base):
        return base, False
    # try compressed version
    base += 'z'
    if os.path.exists(base):
        return base, True
    raise FileNotFoundError


def _make_data_path(prefix, compress):
    res = prefix + SmartPipeWriter.DATA_EXT
    if compress:
        res += 'z'
    return res


def _make_index_path(prefix):
    return prefix + SmartPipeWriter.INDEX_EXT


class SmartPipeWriter:
    INDEX_EXT = ".idx"
    DATA_EXT = ".dat"

    def __init__(self, path_prefix, compress=False):
        self.index_writer = IndexWriter(_make_index_path(path_prefix))
        self.data_path = _make_data_path(path_prefix, compress)
        self._fd = open(self.data_path, mode='wb')
        self._compressor = None
        if compress:
            self._compressor = zlib.compressobj()
            self._compressor_needs_flush = False
        self._raw_ofs = 0

    def close(self):
        if self._fd:
            self._flush()
            self._fd.close()
            self._fd = None
        self.index_writer.close()

    def append(self, key, value):
        k_len = len(key)
        v_len = len(value)
        data = struct.pack("<I", k_len)
        data += key
        data += struct.pack("<I", v_len)
        data += value
        if self._compressor:
            data = self._compressor.compress(data)
            self._compressor_needs_flush = True
        self._fd.write(data)
        self._raw_ofs += 4 + 4 + k_len + v_len

    def checkpoint(self, key):
        self._flush()
        self.index_writer.append(key, self._fd.tell(), self._raw_ofs)

    def _flush(self):
        if self._compressor and self._compressor_needs_flush:
            dat = self._compressor.flush(zlib.Z_FINISH)
            self._fd.write(dat)
            self._compressor = zlib.compressobj()
            self._compressor_needs_flush = False
        self._fd.flush()


class IndexWriter:
    def __init__(self, path):
        self.path = path
        self._entries = 0
        self._fd = self._open_data_stream(path)

    def __str__(self):
        return "IndexWriter[{path}, entries={entries}]".format(path=self.path, entries=self._entries)

    @staticmethod
    def _open_data_stream(path):
        return open(path, "wb")

    def close(self):
        if self._fd:
            self._fd.close()
            self._fd = None

    def append(self, key, ofs, raw_ofs):
        """
        Append entry to index
        :param key: binary key to remember
        :param ofs: offset in data stream which will be associated with that key
        :param raw_ofs: current offset in a raw data stream
        """
        k_len = len(key)
        self._fd.write(struct.pack("<I", k_len))
        self._fd.write(key)
        self._fd.write(struct.pack("<Q", ofs))
        self._fd.write(struct.pack("<Q", raw_ofs))
        self._fd.flush()


class IndexReader:
    def __init__(self, path):
        self.ofs_map, self.keys = IndexReader._read_data(path)

    @staticmethod
    def _read_data(path):
        ofs_map = {}
        keys = []
        with open(path, 'rb') as fd:
            while True:
                val = fd.read(4)
                if len(val) != 4:
                    break
                k_len = struct.unpack("<I", val)[0]
                key = fd.read(k_len)
                ofs, raw_ofs = struct.unpack("<QQ", fd.read(8+8))
                ofs_map[key] = ofs, raw_ofs
                keys.append(key)
        return ofs_map, keys


class ZlibWrapper:
    CHUNK_SIZE = 256

    def __init__(self, path, compressed):
        self.path = path
        self.compressed = compressed
        self._fd = open(self.path, 'rb')
        self._buffer = bytearray()

    def close(self):
        if self._fd:
            self._fd.close()
            self._fd = None

    def read(self, size):
        result = self._buffer[:size]
        self._buffer = self._buffer[size:]
        return result

    def seek(self, ofs):
        self._buffer = bytearray()
        self._fd.seek(ofs)

    def pull_block(self, block_size):
        """
        Read next optionally compressed chunk of data from disk
        :param block_size: size of block in bytes or None for last block
        :return:
        """
        size = block_size if block_size is not None else -1
        self._buffer = self._fd.read(size)
        if self.compressed:
            self._buffer = zlib.decompress(self._buffer)


class SmartPipeReader:
    def __init__(self, path_prefix):
        self.data_path, self.compressed = _detect_data_path(path_prefix)
        self._fd = ZlibWrapper(self.data_path, self.compressed)
        self.index = IndexReader(_make_index_path(path_prefix))
        self._next_key_ofs = 0

    def close(self):
        if self._fd:
            self._fd.close()
            self._fd = None

    def pull_block(self, index_key=None):
        """
        Get list of key,value pairs from next block
        :param index_key: optional key of block to seek
        :return: yield block records
        """
        if index_key is not None:
            if not self._seek(index_key):
                return
        comp_block_size, raw_block_size = self._get_block_sizes()
        self._fd.pull_block(comp_block_size)

        while raw_block_size is None or raw_block_size > 0:
            dat = self._fd.read(4)
            if len(dat) != 4:
                break
            k_len = struct.unpack("<I", dat)[0]
            key = self._fd.read(k_len)
            v_len = struct.unpack("<I", self._fd.read(4))[0]
            val = self._fd.read(v_len)
            if raw_block_size is not None:
                raw_block_size -= 4 + 4 + k_len + v_len
            yield (key, val)
        self._next_key_ofs += 1

    def _get_block_sizes(self):
        """
        Return size of the current block in bytes, both uncompressed and compressed sizes
        :return: tuple of (compressed size, uncompressed size) or None,None if it's a last block
        """
        if self._next_key_ofs+1 >= len(self.index.keys):
            return None, None
        key1, key2 = self.index.keys[self._next_key_ofs:self._next_key_ofs+2]
        comp_ofs1, raw_ofs1 = self.index.ofs_map[key1]
        comp_ofs2, raw_ofs2 = self.index.ofs_map[key2]
        return comp_ofs2-comp_ofs1, raw_ofs2-raw_ofs1

    def get_next_block_key(self):
        """
        Return index key for the next block
        :return: key of the next block or None if we reached end of pipe
        """
        if self._next_key_ofs >= len(self.index.keys):
            return None
        return self.index.keys[self._next_key_ofs]

    def _seek(self, key):
        """
        Perform seek on a given key.
        :param key:
        :return: return true if seek was successfull or not needed
        """
        if key == self.get_next_block_key():
            return True
        ofs = self.index.ofs_map.get(key)
        if ofs is None:
            return False
        self._fd.seek(ofs[0])
        self._next_key_ofs = self.index.keys.index(key)
        return True
