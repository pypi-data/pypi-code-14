import time
import os
import datetime

import exceptions

from base import (
    StorageServiceBase,
    FileStat,
    )


class IOErrorContext(object):
    def __enter__(self):
        return self

    def __exit__(self, type_, value, traceback):
        if type_ is IOError and value:
            errno, errstr = value.args
            for exc in exceptions.ClosetError.__subclasses__():
                if exc.fs_errno == errno:
                    raise exc(errstr)


class FilesystemFileStat(FileStat):
    def __init__(self, statinfo):
        # Extract the raw data from stat
        args = {
            'size': statinfo.st_size,
            'atime': statinfo.st_atime,
            'mtime': statinfo.st_mtime,
            'ctime': statinfo.st_ctime,
        }

        # If birthtime exists, use it
        try:
            args['ctime'] = statinfo.st_birthtime if statinfo.st_birthtime is not None else args['ctime']
        except AttributeError:
            pass

        # Fix times
        for k in ('atime', 'mtime', 'ctime'):
            if args[k] is not None:
                args[k] = time.mktime(datetime.datetime.utcfromtimestamp(int(args[k])).timetuple())

        super(FilesystemFileStat, self).__init__(**args)


class FilesystemStorage(StorageServiceBase):
    def __init__(self, name=None, bucket=None, base_directory=None, *args, **kwargs):
        super(FilesystemStorage, self).__init__(name=name, bucket=bucket, *args, **kwargs)
        self.base_directory = base_directory or '/tmp'

    def _normalize_path(self, filename, external=False):
        filename = super(FilesystemStorage, self)._normalize_path(filename)
        if not external:
            filename = os.path.join(self.base_directory, filename)
            if not filename.startswith(self.base_directory):
                raise exceptions.FileOutsideBaseDirectoryError(filename)
        return filename

    def exists(self, filename):
        return os.path.exists(self._normalize_path(filename))

    def open(self, filename, mode=None):
        mode = mode or 'rb'
        filename = self._normalize_path(filename)
        with IOErrorContext():
            if mode[0] in ('w', 'a') or mode[-1] == '+':
                destination_directory = os.path.dirname(filename)
                if not os.path.exists(destination_directory):
                    os.makedirs(destination_directory)

            return open(filename, mode)

    def stat(self, filename):
        with IOErrorContext():
            return FilesystemFileStat(os.stat(self._normalize_path(filename)))

    def delete(self, filename):
        with IOErrorContext():
            return os.unlink(self._normalize_path(filename))
