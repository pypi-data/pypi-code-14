# -*- coding: utf-8 -*-

from collections import namedtuple
try:
    from typing import List, Iterator, Optional  # NOQA
except ImportError:
    pass

# For typing reasons
import fitsio  # NOQA

__all__ = ['ChunkedAdapter', 'chunks']  # type: List[str]


Chunk = namedtuple('Chunk', ['data', 'slice'])


def chunks(*hdus, **kwargs):
    # type: (*fitsio.HDUBase, **int) -> Iterator[Chunk]
    '''
    High level convenience wrapper for ``ChunkedAdapter``

    This builds a chunked adapter around the given hdu object
    and then yields the chunks
    '''
    adapters = [ChunkedAdapter(hdu) for hdu in hdus]

    # Make sure that each chunk is of equal size
    chunksizes = []
    for adapter in adapters:
        if 'chunksize' in kwargs:
            chunksizes.append(kwargs['chunksize'])
        else:
            memory_limit_mb = kwargs['memory_limit_mb']
            chunksizes.append(adapter._memory_to_lightcurves(memory_limit_mb))
    chunksize = min(chunksizes)

    yielders = [adapter(chunksize=chunksize) for adapter in adapters]

    for every in zip(*yielders):
        if len(every) == 1:
            yield every[0]
        else:
            yield every


class ChunkedAdapter(object):

    def __init__(self, hdu):
        # type: (fitsio.HDUBase) -> None
        self.hdu = hdu

    @property
    def nrows(self):
        # type: () -> int
        return self.hdu.get_info()['dims'][0]

    @property
    def num_images(self):
        # type: () -> int
        return self.hdu.get_info()['dims'][1]

    @property
    def data_type(self):
        # type: () -> int
        return self.hdu.get_info()['img_equiv_type']

    @property
    def lc_bytes(self):
        # type: () -> int
        return self._byte_size(self.data_type) * self.num_images

    def __call__(self, chunksize=None, memory_limit_mb=None):
        # type: (Optional[int], Optional[int]) -> Iterator[Chunk]
        if chunksize is None and memory_limit_mb is None:
            raise ValueError(
                'You must supply either chunksize or memory_limit_mb arguments'
            )

        if chunksize is None:
            chunksize = self._memory_to_lightcurves(memory_limit_mb)

        start = 0
        end = min(start + chunksize, self.nrows)
        while end <= self.nrows:
            chunk = self.hdu[start:end, :]
            yield Chunk(data=chunk, slice=slice(start, end))

            start += chunksize
            end = min(end + chunksize, self.nrows)
            if start >= end:
                break

    def _memory_to_lightcurves(self, memory_mb):
        # type: (int) -> int
        memory_bytes = memory_mb * 1024 * 1024
        return memory_bytes // self.lc_bytes

    def _byte_size(self, data_type):
        # type: (int) -> int
        return {
            32: 4,
            -32: 4,
            -64: 8,
            16: 2,
            20: 2,
        }[data_type]

    def _max_num_lightcurves(self, memory_limit_mb):
        # type: (int) -> int
        memory_limit_bytes = memory_limit_mb * 1024 * 1024
        return memory_limit_bytes / self._byte_size(self.data_type)
