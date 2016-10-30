import os

import magic

from exceptions import (
    FileNotFoundError,
    NoBaseURLError,
    )


class StorageServiceBase(object):
    def __init__(self, name=None, bucket=None, base_url=None, *args, **kwargs):
        self.name = name or 'default'
        self.bucket = bucket or (self.name if bucket is None else None)
        self.base_url = base_url

    def _normalize_path(self, filename, external=False):
        if self.bucket:
            filename = os.path.join(self.bucket, filename)
        if external and self.base_url:
            filename = os.path.join(self.base_url, filename)
        filename = os.path.normpath(filename)
        return filename

    def url_for(self, filename):
        if not self.base_url:
            raise NoBaseURLError("No base URL was provided")

        return self.base_url + '/' + self._normalize_path(filename, external=True)

    def exists(self, filename):
        raise NotImplementedError()

    def open(self, filename, mode=None):
        raise NotImplementedError()

    def stat(self, filename):
        raise NotImplementedError()

    def delete(self, filename):
        raise NotImplementedError()

    def mimetype(self, filename):
        return self.open(filename, mode='rb').mimetype

    @staticmethod
    def mimetype_for(file_obj):
        if not hasattr(file_obj, '_mimetype'):
            pos = file_obj.tell()
            file_obj.seek(0)
            file_obj._mimetype = magic.from_buffer(file_obj.read(1024), mime=True)
            file_obj.seek(pos)
        return file_obj._mimetype


class FileStat(object):
    def __init__(self, size, atime, mtime, ctime):
        self.size = size
        self.atime = atime
        self.mtime = mtime
        self.ctime = ctime
