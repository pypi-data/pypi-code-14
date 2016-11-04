import contextlib
import logging

import sqlalchemy

import chryso.errors

LOGGER = logging.getLogger(__name__)

class Transaction():
    def __init__(self, engine, parent):
        self.engine = engine
        self.parent = parent
        self.resolved = False

    @property
    def depth(self):
        depth = 0
        parent = self.parent
        while parent:
            depth += 1
            parent = parent.parent
        return depth

    def savepoint(self):
        self.execute("SAVEPOINT chryso_{}".format(self.depth) if self.parent else "BEGIN")

    def rollback(self):
        if self.resolved:
            raise Exception("This transaction is already resolved, you cannot roll it back now")
        self.execute("ROLLBACK TO SAVEPOINT chryso_{}".format(self.depth) if self.parent else "ROLLBACK")
        self.resolved = True

    def commit(self):
        if self.resolved:
            raise Exception("This transaction is already resolved, you cannot commit it now")
        self.execute("RELEASE SAVEPOINT chryso_{}".format(self.depth) if self.parent else "COMMIT")
        self.resolved = True

    def execute(self, *args, **kwargs):
        try:
            result = self.engine.execute(*args, **kwargs)
            return result
        except (sqlalchemy.exc.DBAPIError, sqlalchemy.exc.StatementError) as e:
            raise chryso.errors.parse_exception(e)

class Engine():
    def __init__(self, uri, tables, track_queries=False, echo=False, set_timezone=True):
        self.tables        = tables
        self.track_queries = track_queries
        self.transactions  = []
        self._engine       = sqlalchemy.create_engine(
            uri,
            echo=echo,
            isolation_level='AUTOCOMMIT',
            pool_recycle=3600,
        )
        self.queries        = []

        if track_queries:
            # pylint: disable=unused-variable
            @sqlalchemy.event.listens_for(self._engine, 'before_execute')
            def receive_execute(conn, clauseelement, multiparams, params): # pylint: disable=unused-argument
                self.queries.append(clauseelement)

        if set_timezone:
            # pylint: disable=unused-variable
            @sqlalchemy.event.listens_for(sqlalchemy.pool.Pool, 'connect')
            def set_utc(dbapi, record): # pylint: disable=unused-argument
                cursor = dbapi.cursor()
                cursor.execute('SET TIME ZONE UTC')
                cursor.close()

    def create_all(self):
        LOGGER.debug("Creating all tables")
        self.tables.metadata.create_all(self._engine)
        LOGGER.debug("DB tables created")

    def drop_all(self):
        LOGGER.debug("Dropping all database tables")
        self.tables.metadata.drop_all(self._engine)
        LOGGER.debug("All database tables dropped")

    def execute(self, query, *args, **kwargs):
        try:
            return self._engine.execute(query, *args, **kwargs)
        except (sqlalchemy.exc.DBAPIError, sqlalchemy.exc.StatementError) as e:
            raise chryso.errors.parse_exception(e)

    @contextlib.contextmanager
    def atomic(self):
        """
        Transaction context manager.

        Will commit the transaction on successful completion of the block or roll it back on error

        Supports nested usage (via savepoints)
        """
        parent = self.transactions[-1] if self.transactions else None
        transaction = Transaction(self, parent)
        self.transactions.append(transaction)
        transaction.savepoint()

        try:
            yield transaction
        except:
            transaction.rollback()
            raise
        else:
            if not transaction.resolved:
                transaction.commit()
        finally:
            self.transactions.pop()

    def reset(self):
        self.drop_all()
        self.create_all()
        self.reset_queries()

    def reset_queries(self):
        self.queries = []

def store(engine):
    store.engine = engine
store.engine = None

def get():
    return store.engine
