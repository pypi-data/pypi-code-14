import datetime
import re
import time

import enum


Date = datetime.date
Time = datetime.time
Timestamp = datetime.datetime
Binary = buffer


def DateFromTicks(ticks):
    return Date(*time.localtime(ticks)[:3])


def TimeFromTicks(ticks):
    return Time(*time.localtime(ticks)[3:6])


def TimestampFromTicks(ticks):
    return Timestamp(*time.localtime(ticks)[:6])


class Type(enum.Enum):
    STRING = 'string'
    BINARY = 'binary'
    NUMBER = 'number'
    DATETIME = 'datetime'
    ROWID = 'rowid'
    UNKNOWN = 'unknown'

    @classmethod
    def from_header(cls, header):
        header = _clean_header(header)
        header = header.lower()
        try:
            return TYPE_REMAPPING[header]
        except KeyError:
            return cls(header)


header_cleaner = re.compile(r'^(\w+)\(.*\)$')


def _clean_header(header):
    match = header_cleaner.match(header)
    if match:
        header = match.group(1)
    return header


TYPE_REMAPPING = {
    'int': Type.NUMBER,
    'integer': Type.NUMBER,
    'blob': Type.BINARY,
    'dynamic': Type.UNKNOWN,
    'text': Type.STRING,
    'boolean': Type.NUMBER,
    'numeric': Type.NUMBER,
}


STRING = Type.STRING
BINARY = Type.BINARY
NUMBER = Type.NUMBER
DATETIME = Type.DATETIME
ROWID = Type.ROWID
