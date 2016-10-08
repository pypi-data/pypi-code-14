from .base import Base
from .models.log import Log as LogModel


class Log(Base):

    def get_collection(self, queryables=None):
        if queryables:
            items = self.dbsession.query(LogModel).filter_by(**queryables).all()
        else:
            items = self.dbsession.query(LogModel).all()
        return items

    def get(self, id):
        item = self.dbsession.query(LogModel).get(id)
        return item