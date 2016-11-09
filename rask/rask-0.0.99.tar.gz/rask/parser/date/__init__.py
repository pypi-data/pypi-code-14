from calendar import timegm
import udatetime

__all__ = [
    'datetime2timestamp',
    'timestamp2datetime'
]

def datetime2timestamp(arg):
    return timegm(arg.timetuple()) + arg.microsecond/1e6

def timestamp2datetime(arg):
    return udatetime.fromtimestamp(int(arg))
