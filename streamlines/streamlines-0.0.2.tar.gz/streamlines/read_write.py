import os
import json
from contextlib import contextmanager

import io

try:
    from lzma import open as lzma_open
except ImportError:
    try:
        from backports.lzma import open as lzma_open
    except:
        def lzma_open(*args, **kwargs):
            assert False, "Missing lzma. Do `pip install backports.lzma`"

try:
    from bz2 import open as bz2_open
except:
    import bz2

    def bz2_open(*args, **kwargs):
        return bz2.BZ2File(*args, **kwargs)

import gzip, zipfile


@contextmanager
def _zipfile_open(file_path, *args, **kwargs):
    """
    Open function to a ZipFile containing a solitary file.
    """
    with zipfile.ZipFile(file_path, *args, **kwargs) as zf:
        files = zf.namelist()
        assert len(files) == 1, "Zipfile must contain only one file."
        yield zf.open(files[0])


EXT_TO_OPEN = {'.gz': gzip.open,
               '.bz2': bz2_open,
               '.xz': lzma_open,
               '.zip': _zipfile_open}


def _infer_compression_reader(file_name):
    final_ext = os.path.splitext(file_name.lower())[-1]
    return EXT_TO_OPEN.get(final_ext, io.open)


def _get_open(file_path, compression, *args, **kwargs):
    if compression == 'infer':
        return _infer_compression_reader(file_path)
    elif compression is None:
        return io.open
    else:
        fmt = "." + compression
        assert fmt in EXT_TO_OPEN, "Unknown compression type."
        return EXT_TO_OPEN[fmt]


def source(file_path, compression='infer', **kwargs):
    open_f = _get_open(file_path, compression)

    with open_f(file_path, **kwargs) as fp:
        for line in fp:
            s = line.decode() if isinstance(line, bytes) else line
            yield s
