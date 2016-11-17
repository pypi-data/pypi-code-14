# coding: utf-8

import hashlib


def get_hash(file):
    md5 = hashlib.md5()

    with open(file, 'rb') as f:
        buffer = f.read(65535)

        while len(buffer) > 0:
            md5.update(buffer)
            buffer = f.read(65535)

    return md5.hexdigest()
