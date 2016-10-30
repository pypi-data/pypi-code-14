import errno


class ClosetError(Exception):
    fs_errno = None


class FileOutsideBaseDirectoryError(ClosetError):
    pass


class NoBaseURLError(ClosetError):
    pass


class FileNotFoundError(ClosetError):
    fs_errno = errno.ENOENT


class AccessDeniedError(ClosetError):
    fs_errno = errno.EACCES


class NotADirectoryError(ClosetError):
    fs_errno = errno.ENOTDIR


class IsADirectoryError(ClosetError):
    fs_errno = errno.EISDIR


class NoSpaceError(ClosetError):
    fs_errno = errno.ENOSPC


class ReadOnlyError(ClosetError):
    fs_errno = errno.EROFS
