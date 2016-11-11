from functools import partial
try:
    import psycopg2
except:
    from psycopg2cffi import compat
    compat.register()
    import psycopg2
from qubit.config import PGSQL_PARAM

__all__ = ['connection', 'new_connection']

connection = psycopg2.connect(**PGSQL_PARAM)
# for creat a new connection
new_connection = partial(psycopg2.connect, **PGSQL_PARAM)
