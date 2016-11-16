from tempfile import NamedTemporaryFile

from django.db import connections, OperationalError
from django.http import JsonResponse

from . import settings
from . import constants


def get_db_status(request):
    """
    Test Database Access
    """
    db_conn = connections['default']
    try:
        db_conn.cursor()
    except OperationalError:
        db_status = False
    else:
        db_status = True
    return db_status


def get_fs_status(request):
    """
    Test that the File System is writable
    """
    try:
        testfile = NamedTemporaryFile()
        testfile.close()
    except OSError as e:
        fs_status = False
    else:
        fs_status = True
    return fs_status


CHECKERS = {
    constants.DATABASE: get_db_status,
    constants.FILESYSTEM: get_fs_status,
}


def status(request):

    statuses = {name: CHECKERS[name](request) for name in settings.STATUS_CHECKS}

    # TODO(Dom): Caching

    status = 500 if any(not statuses[name] for name in settings.FAILURE_CHECKS) else 200

    return JsonResponse(statuses, status=status)
