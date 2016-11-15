import re
from time import time
from bson.objectid import ObjectId

from ..error import NotExistError
from ..util import Selector
from ..validator import method
from ..model.repo import scheduler as rmodel_sched
from ..model.engine import scheduler as emodel_sched


search_fields = {'notes': 0, 'tasks': 0, 'tags': 0}
search_by_author_fields = {'notes': 0, 'tasks': 0, 'tags': 0}
verify_fields = {
    '_id': 0,
    'name': 0,
    'tags': 0,
    'tasks': 0,
    'notes': 0
}


class SchedulerRepo(object):
    '''
    Provide method to manage schedulers in database

    :param pymongo.MongoClient db: Instance of MongoClient
    '''
    def __init__(self, db):
        self._db = db
        self._coll = db['scheduler']
        self._acc_coll = db['account']

    @method(rmodel_sched.insert)
    def insert_one(self, item):
        '''
        Insert one scheduler

        :param dict item: Scheduler to insert
        :return: Identity of new scheduler
        :rtype: bson.objectid.ObjectId
        :raise jsonschema.exceptions.ValidationError: On item is invalid
        '''

        # padding data
        item['num_user'] = 0
        item['modified'] = int(time())

        emodel_sched.validate_insert(item)

        # save to database
        return self._coll.insert_one(item).inserted_id

    @method(rmodel_sched.insert_many)
    def insert_many(self, items):
        '''
        Insert multi schedulers

        :param list items: List of schedulers
        :return: List of identity of new scheduler
        :rtype: list
        :raise jsonschema.exceptions.ValidationError: On item is invalid
        '''

        # padding data
        for item in items:
            item['num_user'] = 0
            item['modified'] = int(time())

        emodel_sched.validate_insert(items)

        # save to database
        return self._coll.insert_many(items).inserted_ids

    @method(ObjectId)
    def find_by_id(self, id):
        '''
        Find scheduler by identity

        :param bson.objectid.ObjectId id: Identity of scheduler
        :return: Scheduler dictionary on found
        :return: None of not found
        :rtype: dict
        '''

        return self._coll.find_one({'_id': id})

    @method(Selector)
    def search(self, selector=Selector()):
        '''
        Search scheduler match with selector

        :param gwisp.Selector selector: Contains specification to search
        :return: List of dictionary contains essential information of scheduler
              on found
        :return: List with none element not found
        :rtype: list
        '''

        filters = {}
        if selector.keyword is not None:
            filters = self._gen_filter(selector.keyword)

        cursor = self._coll.find(filters,
                                 search_fields,
                                 skip=selector.skip,
                                 limit=selector.page_size)

        if cursor.count(with_limit_and_skip=True) == 0:
            return None
        return list(cursor)

    @method(ObjectId, Selector)
    def search_by_author(self, author_id, selector=Selector()):
        '''
        Search by author identity and match with selector

        :param bson.objectid.ObjectId author_id: Author identity
        :param gwisp.Selector selector: Contains specification to search
        :return: List of dictionary contains essential information of scheduler
              on found
        :return: List with none element not found
        :rtype: list
        '''

        filters = {'$and': [{'author._id': author_id}]}
        if selector.keyword is not None:
            filters['$and'].append(self._gen_filter(selector.keyword))

        cursor = self._coll.find(
            filters,
            search_by_author_fields,
            skip=selector.skip,
            limit=selector.page_size
        )

        if cursor.count(with_limit_and_skip=True) == 0:
            return None
        return list(cursor)

    @method(ObjectId, rmodel_sched.update)
    def update_one(self, id, item):
        '''
        Update one scheduler

        :param bson.ObjectId id: Scheduler identity
        :param dict item: Scheduler to update, must contain _id fields
        :raise jsonschema.exceptions.ValidationError: On item is invalid
        '''

        # padding data
        item['modified'] = int(time())

        emodel_sched.validate_update(item)

        result = self._coll.update_one({'_id': id}, {'$set': item})

        if result.matched_count == 0:
            raise NotExistError('Scheduler is not exist')

    @method(ObjectId)
    def delete_one(self, id):
        '''
        Delete one scheduler

        :param bson.objectid.ObjectId id: Identity of scheduler to delete
        :raise gwisp.error.NotExistError: On scheduler is not exist
        '''

        result = self._coll.delete_one({'_id': id})

        if result.deleted_count == 0:
            raise NotExistError('Scheduler is not exist')

    @method(ObjectId)
    def is_exist(self, id):
        '''
        Verify that scheduler is exist

        :param bson.objectid.ObjectId id: Identity of scheduler
        :return: True on scheduler is exist
        :return: False on scheduler is not exist
        :rtype: bool
        '''

        return self._coll.find_one({'_id': id}, verify_fields) is not None

    def count(self):
        '''
        Count number of schedulers

        :return: Number of schedulers in collection
        :rtype: int
        '''

        return self._coll.count()

    def _gen_filter(self, keyword):
        '''
        Generate query filter of mongodb

        :param str keyword: Keyword to search
        :return: Filter
        :rtype: dict
        '''
        return {'$or': [
            {'name': {'$regex': re.compile(keyword)}},
            {'tags': {
                '$elemMatch': {
                    '$regex': re.compile(keyword)
                }
            }}
        ]}
