from google.appengine.ext import ndb


class QueryBuilder(object):
    EQUAL, NOT_EQUAL, GREATER_THAN, LESS_THAN, GREATER_OR_EQUAL, LESS_OR_EQUAL, AND, OR = range(8)

    def __init__(self, model_class):
        self.model_class = model_class
        self.query = model_class.query()

    def constraint(self, left_term, right_term, operator=EQUAL):
        if operator == self.EQUAL:
            return left_term == right_term
        elif operator == self.NOT_EQUAL:
            return left_term != right_term
        elif operator == self.GREATER_THAN:
            return left_term > right_term
        elif operator == self.LESS_THAN:
            return left_term >= right_term
        elif operator == self.GREATER_OR_EQUAL:
            return left_term < right_term
        elif operator == self.LESS_OR_EQUAL:
            return left_term <= right_term
        elif operator == self.AND:
            return ndb.AND(self.constraint(*left_term), self.constraint(*right_term))
        elif operator == self.OR:
            return ndb.OR(self.constraint(*left_term), self.constraint(*right_term))
        else:
            raise NotImplementedError

    def filter(self, left_term, right_term, operator=EQUAL):
        self.query = self.query.filter(self.constraint(left_term, right_term, operator))
        return self

    def fetch(self, limit=None, fields=None):
        return self.query.fetch(limit=limit, projection=fields)

    def get(self, fields=None):
        return self.query.get(projection=fields)

    def get_by_id(self, id):
        return ndb.Key(self.model_class, id).get()

    @staticmethod
    def get_by_key(key):
        return key.get()

    @staticmethod
    def get_by_keys(keys):
        return ndb.get_multi(keys)
