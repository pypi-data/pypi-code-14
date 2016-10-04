try:
    from pysqlite2 import dbapi2 as DB
except ImportError:
    import sqlite3 as DB

def connect(*args, **kwargs):
    if not args:
        args += tuple((':memory:',))
    return DB.connect(*args, **kwargs)
