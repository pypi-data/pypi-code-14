import datetime
from os.path import expanduser
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base

home = expanduser('~')
db_url = 'sqlite:///' + home + "/.words.db"
db = create_engine(db_url)
Base = declarative_base()


class Record(Base):
    __tablename__ = 'records'

    id = Column(Integer, primary_key=True)
    word = Column(String, unique=True)
    means = Column(String(256))
    number = Column(Integer, default=1)
    uptime = Column(DateTime, default=datetime.datetime.now)

    def __repr__(self):
        return str(self.id) + "\t" + self.word + "\t" + str(self.number)


Base.metadata.create_all(db)
