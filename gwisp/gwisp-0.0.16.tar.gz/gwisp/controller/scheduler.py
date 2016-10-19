from falcon import HTTP_204, HTTPBadRequest
from bson.objectid import ObjectId
from ..repo import SchedulerRepo
from ..util import parse_selector


class SchedulerCtl(object):
    '''
    Scheduler resource

    :param pymongo.MongoClient db: Instance of mongo client
    :param gwisp.Protector protector: Instance of protector
    '''

    def __init__(self, db, protector):
        self._protector = protector
        self._repo = SchedulerRepo(db)

    def on_get(self, req, res):
        '''
        Search scheduler

        Request: Query parameters as selector

        Response: List of scheduler match with selector
        '''

        res.body = self._repo.search(parse_selector(req))

    def on_post(self, req, res):
        '''
        Create new scheduler

        Request: Scheduler in body, access token in header

        Response: Relative location of new scheduler in header, field
            Location
        '''

        if req.context['body'] is None:
            raise HTTPBadRequest('Invalid body', 'Body is empty')

        auth = self._protector.check(req)

        item = req.context['body']
        item['author'] = auth.account_id
        id = self._repo.insert_one(item)

        res.status = HTTP_204
        res.set_header('Location', '/scheduler/{}'.format(str(id)))


class SchedulerItemCtl(object):
    '''
    Scheduler resource

    :param pymongo.MongoClient db: Instance of mongo client
    :param gwisp.Protector protector: Instance of protector
    '''

    def __init__(self, db, protector):
        self._repo = SchedulerRepo(db)
        self._protector = protector

    def on_get(self, req, res, id):
        '''
        Query single scheduler

        Request: Identify of scheduler in request url

        Response: Scheduler in body
        '''

        res.body = self._repo.find_by_id(ObjectId(id))

    def on_delete(self, req, res, id):
        '''
        Remove scheduler

        Request: Identify of scheduler in request url
        '''

        self._protector.check(req, False, 'root')
