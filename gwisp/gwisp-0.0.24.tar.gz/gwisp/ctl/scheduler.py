from falcon import HTTP_204, HTTP_404, \
                   HTTPBadRequest, HTTPNotFound, HTTPForbidden
from bson.objectid import ObjectId

from ..error import NotExistError
from ..model.front.post_scheduler import validate_post
from ..model.front.put_scheduler import validate_put
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

        if res.body is None:
            res.status = HTTP_404

    def on_post(self, req, res):
        '''
        Create new scheduler

        Request: Scheduler in body, access token in header

        Response: Relative location of new scheduler in header, field
            Location
        '''

        if 'body' not in req.context:
            raise HTTPBadRequest('400 Bad Request', 'Body is empty')
        item = req.context['body']
        validate_post(item)

        auth = self._protector.check(req, iacc=True)

        # padding data
        item['author'] = {
            '_id': auth.account_id,
            'name': auth.account['name']
        }

        # save scheduler to storage
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

        sched_id = None
        try:
            sched_id = ObjectId(id)
        except Exception as e:
            raise HTTPBadRequest(
                title='400 HTTPBadRequest',
                description='id is invalid'
            )

        res.body = self._repo.find_by_id(sched_id)

        if res.body is None:
            raise HTTPNotFound(
                title='404 Not Found',
                description='Not found scheduler'
            )

    def on_put(self, req, res, id):
        '''
        Update scheduler

        Request:
            - Identify of scheduler in request url
            - Scheduler content in body
            - Authorization header

        Response: No Content
        '''

        sched_id = None
        try:
            sched_id = ObjectId(id)
        except Exception as e:
            raise HTTPBadRequest(
                title='400 HTTPBadRequest',
                description='id is invalid'
            )

        auth = self._protector.check(req)
        old_item = self._repo.find_by_id(sched_id)
        if old_item is None:
            raise NotExistError('Scheduler is not exist')
        if old_item['author']['_id'] != auth.account_id:
            raise HTTPForbidden(
                title='403 Forbidden',
                description='Can not update item of other account'
            )

        if 'body' not in req.context:
            raise HTTPBadRequest('400 Bad Request', 'Invalid body')
        item = req.context['body']
        validate_put(item)

        # put data to storage
        self._repo.update_one(ObjectId(id), item)

        # result is no content
        res.status = HTTP_204

    def on_delete(self, req, res, id):
        '''
        Remove scheduler

        Request: Identify of scheduler in request url
        '''

        # authenticate
        auth = self._protector.check(req)

        # ensure item is exist
        item = self._repo.find_by_id(ObjectId(id))
        if item is None:
            raise HTTPNotFound(description='Scheduler is not exist')

        # ensure only owner have permission to delete item
        if item['author']['_id'] != auth.account_id:
            raise HTTPForbidden(
                title='403 Forbidden',
                description='Can not delete item of other account'
            )

        # remove item from storage
        self._repo.delete_one(ObjectId(id))

        # result is no content
        res.status = HTTP_204
