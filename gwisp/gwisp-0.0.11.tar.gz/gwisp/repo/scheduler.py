import re
from ..model.scheduler import validate_insert, validate_update
from ..error import NotExistError
from ..util import Selector


search_fields = {'notes': 0, 'tasks': 0, 'tags': 0}
verify_fields = {
    '_id': 0,
    'name': 0,
    'tags': 0,
    'tasks': 0,
    'notes': 0
}


class SchedulerRepo(object):
    '''
    Provide method to query scheduler in mongodb

    :param pymongo.MongoClient db: Instance of MongoClient
    '''
    def __init__(self, db):
        self._db = db
        self._coll = db['scheduler']
        self._acc_coll = db['account']

    def find_by_id(self, id):
        '''
        Find scheduler by identity

        :param bson.objectid.ObjectId id: Identity of scheduler
        :return: Scheduler dictionary on found
        :return: None of not found
        :rtype: dict
        '''
        return self._coll.find_one({'_id': id})

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
        return list(cursor)

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

        filters = {'$and': [{'author': author_id}]}
        if selector.keyword is not None:
            filters['$and'].append(self._gen_filter(selector.keyword))

        cursor = self._coll.find(filters,
                                 search_fields,
                                 skip=selector.skip,
                                 limit=selector.page_size)

        return list(cursor)

    def search_by_id(self, ids):
        '''
        Search by list of identity of schedulers

        :param list ids: List of identity of schedulers
        :return: List of dictionary contains essential information of scheduler
              on found
        :return: List with none element not found
        :rtype: list
        '''

        filters = {'_id': {'$in': ids}}

        cursor = self._coll.find(filters, search_fields)

        return list(cursor)

    def insert_one(self, item):
        '''
        Insert one scheduler

        :param dict item: Scheduler to insert
        :return: Identity of new scheduler
        :rtype: bson.objectid.ObjectId
        '''

        validate_insert(item)

        if (not self._acc_is_exist(item['author'])):
            raise NotExistError('account is not exists')

        return self._coll.insert_one(item).inserted_id

    def insert_many(self, items):
        '''
        Insert many schedulers

        :param list items: List of schedulers
        :return: List of identity of new scheduler
        :rtype: list
        '''

        validate_insert(items)

        author_ids = []
        for item in items:
            if item['author'] not in author_ids:
                author_ids.append(item['author'])
        if (not self._acc_is_exist(author_ids)):
            raise NotExistError('account is not exists')

        return self._coll.insert_many(items).inserted_ids

    def update_one(self, item):
        '''
        Update one scheduler

        :param dict item: Scheduler to update, must contain _id fields
        '''

        validate_update(item)
        id = item['_id']
        del item['_id']

        return self._coll.update_one({'_id': id}, {'$set': item})

    def delete_one(self, id):
        '''
        Delete one scheduler

        :param bson.objectid.ObjectId id: Identity of scheduler to delete
        '''

        return self._coll.delete_one({'_id': id})

    def is_exist(self, id):
        '''
        Verify that scheduler is exist

        :param id: Identity of scheduler
        :type id: bson.objectid.ObjectId
        :return: True on scheduler is exist
        :return: False on scheduler is not exist
        :rtype: bool
        '''

        return self._coll.find_one({'_id': id}, verify_fields) is not None

    def _acc_is_exist(self, ids):
        '''
        Verify list of account is exist

        :param ids: List of account identity
        :type ids: list
        :return: True on all of account is exist
        :return: False on one or more account is not exist
        :rtype: bool
        '''

        if type(ids) is list:
            cursor = self._acc_coll.find({'_id': {'$in': ids}})
            return cursor.count() == len(ids)
        else:
            return self._acc_coll.find_one({'_id': ids}) is not None

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
