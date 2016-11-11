from qubit.io.postgres import connection as conn
from postgresql.driver.pq3 import Connection

__all__ = ['execute_file']


def execute_file(filename: str, conn: Connection=conn) -> Connection:
    '''
    Execute a SQL file
    '''
    with open(filename, 'r') as f:
        cur = conn.cursor()
        data = ''.join(map(lambda l: l.strip(), f.readlines()))
        [cur.execute(q) or print(q) for q in data.split(';') if q]
        conn.commit()
        return conn
