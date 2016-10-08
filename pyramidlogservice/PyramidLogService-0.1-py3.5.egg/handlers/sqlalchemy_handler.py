import logging
import traceback
import transaction
from ..models.log import Log
from ..models import get_engine, get_session_factory, get_tm_session
from pyramid.threadlocal import get_current_registry


class SQLAlchemyHandler(logging.Handler):
    @staticmethod
    def get_log_db_session():
        import transaction
        settings = get_current_registry().settings
        engine = get_engine(settings)
        session_factory = get_session_factory(engine)
        return get_tm_session(session_factory, transaction.manager)

    # A very basic logger that commits a LogRecord to the SQL Db
    def emit(self, record):
        trace = None
        exc = record.__dict__['exc_info']
        if exc:
            trace = logging.Formatter('', exc).format(record)
        log = Log(
            logger=record.__dict__['name'],
            level=record.__dict__['levelname'],
            trace=trace,
            msg=record.__dict__['msg'],)
        dbsession = self.get_log_db_session()
        dbsession.add(log)
        transaction.commit()
