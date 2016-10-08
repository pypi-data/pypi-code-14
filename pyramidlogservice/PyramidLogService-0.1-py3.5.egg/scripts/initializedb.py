from sqlalchemy import create_engine

from logservice import models
from logservice.models.meta import Base
from sqlalchemy.orm import sessionmaker


class InitializeDb(object):
    def __init__(self, connection_string, dbsession=None):
        self.connection_string = connection_string
        self.dbsession = dbsession

    def initialize_db(self):
        if self.dbsession is None:
            engine = create_engine(self.connection_string)
            Base.metadata.drop_all(engine)
            Base.metadata.create_all(engine)

            # create a configured "Session" class
            Session = sessionmaker(bind=engine)

            # create a Session
            dbsession = Session()
        else:
            dbsession = self.dbsession

        # http://docs.python.org/howto/logging.html#configuring-logging
        import logging

        # create logger
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)

        # create console handler and set level to debug
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        # create formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # add formatter to ch
        ch.setFormatter(formatter)

        # add ch to logger
        logger.addHandler(ch)

        # 'application' code
        logger.debug('Initializing Logs')
        from ..models.log import Log
        lg = Log(msg='Initializing Logs')
        dbsession.add(lg)
        dbsession.commit()
