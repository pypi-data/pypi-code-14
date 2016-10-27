import base64
from collections import namedtuple
import urlparse

import requests

from festung._private import cast
from festung._private import no_password_url
from festung._private import to_http_url
# Exceptions have to be on the DBAPI module
from festung.exceptions import DatabaseError      # NOQA
from festung.exceptions import DataError          # NOQA
from festung.exceptions import Error              # NOQA
from festung.exceptions import IntegrityError     # NOQA
from festung.exceptions import InterfaceError     # NOQA
from festung.exceptions import InternalError      # NOQA
from festung.exceptions import NotSupportedError  # NOQA
from festung.exceptions import OperationalError   # NOQA
from festung.exceptions import ProgrammingError   # NOQA
from festung.exceptions import Warning            # NOQA
import festung.types
# Types have to be on the DBAPI module
from festung.types import BINARY                  # NOQA
from festung.types import Binary                  # NOQA
from festung.types import Date                    # NOQA
from festung.types import DateFromTicks           # NOQA
from festung.types import DATETIME                # NOQA
from festung.types import NUMBER                  # NOQA
from festung.types import ROWID                   # NOQA
from festung.types import STRING                  # NOQA
from festung.types import Time                    # NOQA
from festung.types import TimeFromTicks           # NOQA
from festung.types import Timestamp               # NOQA


__all__ = ['connect', 'apilevel', 'paramstyle', 'threadsafety', 'Connection', 'Cursor']


apilevel = '2.0'
threadsafety = 3  # Threads may share the module, connections and cursors
paramstyle = 'qmark'

SCHEME = 'festung'


class Connection(object):
    def __init__(self, url):
        parsed_url = urlparse.urlparse(url)
        if parsed_url.scheme != SCHEME:
            raise ValueError("We only support festung:// connections.")
        self.url = url

    def close(self):
        pass

    def commit(self):
        # TODO(Antoine): Implement
        pass

    def rollback(self):
        # TODO(Antoine): Implement
        pass

    def cursor(self):
        return Cursor(self)

    @property
    def _http_url(self):
        return to_http_url(self.url)

    @property
    def _password(self):
        parsed_url = urlparse.urlsplit(self.url)
        return parsed_url.password or ''

    def _request(self, method, **kwargs):
        headers = kwargs.pop('headers', {})
        headers['Authorization'] = base64.b64encode(self._password)
        kwargs['headers'] = headers
        resp = requests.request(method, self._http_url, **kwargs)
        resp.raise_for_status()
        return resp.json()

    def __repr__(self):
        return "<Connection({})>".format(no_password_url(self.url))


connect = Connection


CursorDescription = namedtuple(
    'CursorDescription', 'name,type_code,display_size,internal_size,precisison,scale,null_ok')


NO_EXECUTE_ROWCOUNT = -1  # <https://www.python.org/dev/peps/pep-0249/#rowcount>
NO_EXECUTE_DESCRIPTION = None  # <https://www.python.org/dev/peps/pep-0249/#description>
NO_MORE_ROW = None  # <https://www.python.org/dev/peps/pep-0249/#fetchone>
NO_EXECUTE_ITER = object()


def _generate_description(headers):
    names = [h['name'] for h in headers]
    # FIXME(Antoine): This is not row you're supposed to infer SQL types
    type_codes = [festung.types.Type.from_header(h['type']) for h in headers]

    # TODO(Antoine): Read more description attributes
    all_none = [None] * len(headers)
    display_sizes = all_none
    internal_sizes = all_none
    precisions = all_none
    scales = all_none
    null_ok = all_none

    all_args = zip(names, type_codes, display_sizes, internal_sizes, precisions, scales, null_ok)
    return [CursorDescription(*args) for args in all_args]


class Cursor(object):
    def __init__(self, connection):
        self.connection = connection
        self._iter = NO_EXECUTE_ITER
        self._description = NO_EXECUTE_DESCRIPTION
        self._rowcount = NO_EXECUTE_ROWCOUNT
        self._arraysize = 1
        self.lastrowid = 0

    @property
    def description(self):
        return self._description

    @property
    def rowcount(self):
        return self._rowcount

    @property
    def arraysize(self):
        return self._arraysize

    @arraysize.setter
    def arraysize(self, value):
        if not isinstance(value, (int, long)):
                raise ValueError("arraysize should be an integer")
        self._arraysize = value

    def callproc(self, procname, parameters=None):
        parameters = parameters or []
        raise NotImplementedError

    def execute(self, operation, parameters=None):
        parameters = parameters or []
        data = dict(sql=operation, params=[cast(p) for p in parameters])
        res = self._request('POST', json=data)
        # For debugging purposes
        self._data = res
        # FIXME(moritz): Also handle if res contains `type` (i.e. operational errors)
        if 'errors' in res:
            raise DataError(res['message'], errors=res['errors'])
        self._iter = iter(res['data'])
        self.lastrowid = res['last_row_id']
        # FIXME(Antoine): I'm not sure that's the way to implement rowcount...
        self._rowcount = res['rows_changed']

        self._description = _generate_description(res['headers'])

    def executemany(self, operation, parameters_sequence):
        for parameters in parameters_sequence:
            self.execute(operation, parameters)
            if self.fetchone() is not NO_MORE_ROW:
                raise ProgrammingError("The statement shall not produce a result.")

    def fetchone(self):
        if self._iter is NO_EXECUTE_ITER:
            raise ProgrammingError("No statement was executed on this cursor.")
        try:
            return tuple(next(self._iter))
        except StopIteration:
            return NO_MORE_ROW

    def fetchmany(self, size=None):
        if size is None:
            size = self.arraysize

        acc = []
        for _ in range(size):
            row = self.fetchone()
            if row is NO_MORE_ROW:
                break
            acc.append(row)
        return acc

    def fetchall(self):
        # FIXME(Antoine): This is very similar to fetchmany(), this should be
        #                 refactor in one function.
        acc = []
        while True:
            row = self.fetchone()
            if row is NO_MORE_ROW:
                break
            acc.append(row)
        return acc

    def nextset(self):
        raise NotImplementedError

    def setinputsize(sizes):
        raise NotImplementedError

    def setoutputsize(size, columns=None):
        raise NotImplementedError

    @property
    def rownumber(self):
        raise NotImplementedError

    def close(self):
        pass

    def _request(self, *args, **kwargs):
        return self.connection._request(*args, **kwargs)
