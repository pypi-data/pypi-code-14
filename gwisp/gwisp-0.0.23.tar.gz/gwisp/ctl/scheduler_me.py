from falcon import HTTPNotFound

from ..repo import SchedulerRepo
from ..util import parse_selector


class SchedulerMeCtl(object):
    '''
    Allow search scheduler by author

    :param pymongo.MongoClient db: Instance of connection to mongodb server
    :param gwisp.Protector protector: Instance of protector
    '''

    def __init__(self, db, protector):
        self._repo = SchedulerRepo(db)
        self._protector = protector

    def on_get(self, req, res):
        auth = self._protector.check(req)
        selector = parse_selector(req)

        res.body = self._repo.search_by_author(auth.account_id, selector)
        if len(res.body) == 0:
            raise HTTPNotFound(
                title='404 Not Found',
                description='Not found scheduler'
            )
