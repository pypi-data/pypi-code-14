#-*- coding:utf-8 -*-
import os
import tempfile
import six
from django.utils.encoding import (
    force_bytes, force_str, python_2_unicode_compatible, smart_text,
)
from django.core.files.base import File


class QiniuFile(File):
    def __init__(self, name, qiniu_storage, mode):
        self._storage = qiniu_storage
        self._name = name[len(self._storage.location):].lstrip('/')
        self._mode = mode
        self.file = tempfile.TemporaryFile()
        self._is_dirty = False
        self._is_read = False

    @property
    def size(self):
        if self._is_dirty or self._is_read:
            # Get the size of a file like object
            # Check http://stackoverflow.com/a/19079887
            old_file_position = self.file.tell()
            self.file.seek(0, os.SEEK_END)
            self._size = self.file.tell()
            self.file.seek(old_file_position, os.SEEK_SET)
        if not hasattr(self, '_size'):
            self._size = self._storage.size(self._name)
        return self._size

    def read(self, num_bytes=None):
        if not self._is_read:
            content = self._storage._read(self._name)
            self.file = six.BytesIO(content)
            self._is_read = True

        if num_bytes is None:
            data = self.file.read()
        else:
            data = self.file.read(num_bytes)

        if 'b' in self._mode:
            return data
        else:
            return force_text(data)

    def write(self, content):
        if 'w' not in self._mode:
            raise AttributeError("File was opened for read-only access.")

        self.file.write(force_bytes(content))
        self._is_dirty = True
        self._is_read = True

    def close(self):
        if self._is_dirty:
            self.file.seek(0)
            self._storage._save(self._name, self.file)
        self.file.close()


class QiniuImageFile(File):
    pass
