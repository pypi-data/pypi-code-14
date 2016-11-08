'''
Copyright (C) 2015-2016 Skylable Ltd. <info-copyright@skylable.com>
License: Apache 2.0, see LICENSE for more details.
'''

from __future__ import unicode_literals

import hashlib
from typing import Iterable, Tuple  # noqa

from sxclient.tools.string_helpers import tobytes

__all__ = ['generate_blocks']


def generate_blocks(block_size, cluster_uuid, content):
    # type: (int, str, str) -> Iterable[Tuple[str, bytes]]
    '''
    Generate blocks based on block_size, cluster_uuid and content.

    It's a generator of (hash, chunk) pairs ready to be uploaded.
    '''

    cursor = 0
    cluster_uuid_bytes = tobytes(cluster_uuid)
    content_bytes = tobytes(content)
    chunk = content_bytes[cursor:cursor+block_size]
    while chunk:
        size_diff = block_size - len(chunk)
        if size_diff > 0:
            chunk += b'\0' * size_diff
        chunk_name = hashlib.sha1(cluster_uuid_bytes + chunk).hexdigest()
        yield chunk_name, chunk
        cursor += block_size
        chunk = content_bytes[cursor:cursor+block_size]
