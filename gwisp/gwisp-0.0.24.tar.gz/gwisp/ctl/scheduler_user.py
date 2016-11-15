from falcon import HTTPNotFound, HTTPBadRequest
from bson import ObjectId

from ..repo import CSchedulerRepo
from ..util import parse_selector


class SchedulerUserCtl(object):
    '''
    Allow search schedulers on user view

    :param pymongo.MongoClient db: Instance of connection to mongodb server
    :param gwisp.Protector protector: Instance of protector
    '''

    def __init__(self, db, protector):
        self._protector = protector
        self._repo = CSchedulerRepo(db)

    def on_get(self, req, res):
        auth = self._protector.check(req)

        selector = parse_selector(req)

        res.body = self._repo.search_on_uview(auth.account_id, selector)
        if res.body is None:
            raise HTTPNotFound(description='Not found scheduler')


class SchedulerUserItemCtl(object):
    '''
    Allow query single shceduler on user view point

    :param pymongo.MongoClient db: Instance of connection to mongodb server
    :param gwisp.Protector protector: Instance of protector
    '''

    def __init__(self, db, protector):
        self._protector = protector
        self._repo = CSchedulerRepo(db)

    def on_get(self, req, res, id):
        auth = self._protector.check(req)

        try:
            sched_id = ObjectId(id)
        except Exception:
            raise HTTPBadRequest(
                title='400 Bad Request',
                description='Identity is invalid'
            )

        res.body = self._repo.find_by_id_on_uview(auth.account_id, sched_id)
        if res.body is None:
            raise HTTPNotFound(
                title='404 Not Found',
                description='Not found scheduler'
            )
