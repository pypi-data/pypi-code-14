import re
import copy
from math import ceil
from datetime import datetime

from .scheduler import SchedulerRepo

from ..error import NotExistError
from ..model.cscheduler import validate_insert


search_by_author_fields = {
    'tags': 0, 'tasks': 0, 'notes': 0
}
search_by_cloner_fields = {
    'tags': 0, 'tasks': 0, 'notes': 0, '_cloner': 0,
    'modified': 0
}


class CSchedulerRepo(object):
    '''
    Query cloned scheduler on user view

    :param pymongo.MongoClient db: Instance of connection to mongdb server
    '''
    def __init__(self, db):
        self._sched_repo = SchedulerRepo(db)
        self._sched_coll = db['scheduler']
        self._csched_coll = db['cscheduler']
        self._acc_coll = db['account']

    def search(self, account_id, selector):
        '''
        Search scheduler on view of account which have account_id.
        Support selector

        :param bson.ObjectId account_id: Identity of account
        :param gwisp.Selector selector: Keyword and pagging information
        :return: List of scheduler match with selector. Each items have
            more extra properties on user view
        :rtype: list
        :rtype: None
        '''

        # search scheduler
        real_items = self._sched_repo.search(selector)

        # search cloned scheduler of account
        real_ids = [i['_id'] for i in real_items]
        cloned_cusor = self._csched_coll.find({
            '_cloner': account_id,
            '_id': {'$in': real_ids}
        })
        cloned_items = list(cloned_cusor)

        # compare real and cloned scheduler to mark '_cloned' and '_updated'
        cloned_ids = [i['_id'] for i in cloned_items]
        cloned_index = {i['_id']: i for i in cloned_items}
        for item in real_items:
            if item['_id'] not in cloned_ids:
                item['_cloned'] = False
                item['_updated'] = False
                continue

            item['_cloned'] = True
            cloned_item = cloned_index[item['_id']]
            if item['modified'] > cloned_item['_cloned_date']:
                item['_updated'] = False
            else:
                item['_updated'] = True

        return real_items

    def search_by_cloner(self, acc_id, selector):
        '''
        Search scheduler cloned by account

        :param bson.ObjectId acc_id: Account identity
        :param gwisp.Selector selector: Search information
        '''

        filters = {'$and': [{'_cloner': acc_id}]}
        if selector.keyword is not None:
            filters['$and'].append(self._gen_filter(selector.keyword))

        cloned_cusor = self._csched_coll.find(
            filters,
            search_by_cloner_fields,
            skip=selector.skip,
            limit=selector.page_size
        )
        cloned_items = list(cloned_cusor)

        cloned_ids = [i['_id'] for i in cloned_items]
        real_items = self._sched_coll.find(
            {'_id': {'$in': cloned_ids}},
            {'notes': 0, 'tags': 0, 'tasks': 0, 'author': 0, 'num_user': 0}
        )

        real_indexs = {i['_id']: i['modified'] for i in real_items}
        for item in cloned_items:
            if real_indexs[item['_id']] > item['_cloned_date']:
                item['_updated'] = False
            else:
                item['_updated'] = True

        return cloned_items

    def find_by_id(self, acc_id, sched_id):
        '''
        Find one scheduler on view of account which have acc_id

        :param bson.ObjectId acc_id: Account identity
        :return dict: Scheduler object
        :rtype: dict
        '''

        real_item = self._sched_repo.find_by_id(sched_id)
        if real_item is None:
            raise NotExistError('Scheduler is not exists')

        cloned_item = self._csched_coll.find_one({
            '_id': sched_id,
            '_cloner': acc_id
        })

        if cloned_item is None:
            real_item['_cloned'] = False
            real_item['_updated'] = False
            return real_item

        real_item['_cloned'] = True
        if real_item['modified'] > cloned_item['_cloned_date']:
            real_item['_updated'] = False
        else:
            real_item['_updated'] = True

        return real_item

    def find_by_cloner_and_id(self, cloner, id):
        '''
        Find cloned scheduler by cloner and identity

        :param bson.ObjectId cloner: Cloner identity
        :param bson.ObjectId id: Scheduler identity
        :return: Scheduler cloned
        :rtype: dict
        '''

        real_item = self._sched_repo.find_by_id(id)
        if real_item is None:
            return None

        cloned_item = self._csched_coll.find_one(
            {'_id': id, '_cloner': cloner}
        )
        if cloned_item is None:
            return None

        if real_item['modified'] > cloned_item['_cloned_date']:
            cloned_item['_updated'] = False
        else:
            cloned_item['_updated'] = True

        return cloned_item

    def clone_one(self, acc_id, item):
        '''
        Create an cloned scheduler belong account if it is not early exist.
        Replace data of scheduler if it is early exist

        :param bson.ObjectId acc_id: Account identity
        :param dict item: Scheduler to clone
        '''

        # padding data
        clone_item = copy.deepcopy(item)
        clone_item['_cloner'] = acc_id
        clone_item['_cloned_date'] = int(datetime.now().timestamp())

        # validate data
        validate_insert(clone_item)

        # verify item is early exist
        key = {
            '_id': clone_item['_id'],
            '_cloner': acc_id
        }
        old_item = self._csched_coll.find_one(key)

        # update or insert to storage
        if old_item is None:
            self._csched_coll.insert_one(clone_item)
        else:
            self._csched_coll.update_one(key, {'$set': clone_item})

    def use_scheduler(self, acc_id, sched_id):
        '''
        Make account with acc_id use use scheduler which have sched_id.
        If scheduler is not cloned, clone it.
        Then copy cloned version to account.scheduler

        :param bson.ObjectId acc_id: Account identity
        :param bson.ObjectId sched_id: Scheduler identity
        '''

        cloned_item = self._csched_coll.find_one({
            '_cloner': acc_id,
            '_id': sched_id
        })

        # Clone new item
        if cloned_item is None:
            cloned_item = self._sched_repo.find_by_id(sched_id)
            if cloned_item is None:
                raise NotExistError('Scheduler is not exists')

            cloned_item['_cloner'] = acc_id
            cloned_item['_cloned_date'] = int(datetime.now().timestamp())

            self._csched_coll.insert_one(cloned_item)

        # Copy cloned version to account.scheduler
        del cloned_item['_cloner']
        self._acc_coll.update_one(
            {'_id': acc_id},
            {'$set': {'scheduler': cloned_item}}
        )

    def update_cloner(self, account_id):
        '''
        Update all of cloned scheduler belong account with newest data

        :param bson.ObjectId account_id: Account identity
            by account
        '''

        # find scheduler is using by account
        account = self._acc_coll.find_one(
            {'_id': account_id},
            {'email': 0, 'avatar': 0, 'groups': 0, 'subject': 0}
        )
        if account is None:
            raise NotExistError('Account is not exist')

        # prepare for cloned schedulers
        number_item = self._csched_coll.count({'_cloner': account_id})
        page_size = 16
        number_of_page = ceil(number_item / page_size)

        # clone each page of scheduler
        for page_index in range(number_of_page):
            # query page of cloned schedulers
            cloned_cusor = self._csched_coll.find(
                {'_cloner': account_id},
                {
                    'tags': 0, 'tasks': 0, 'notes': 0, 'author': 0,
                    'modified': 0
                },
                skip=page_index*page_size,
                limit=page_size
            )
            cloned_items = list(cloned_cusor)

            # query page of real schedulers
            cloned_ids = [i['_id'] for i in cloned_items]
            real_cusor = self._sched_coll.find(
                {'_id': {'$in': cloned_ids}}
            )
            real_items = list(real_cusor)

            # find scheduler is using by account then update
            # and padding meta data for each real schedulers
            for item in real_items:
                item['_cloned_date'] = int(datetime.now().timestamp())

                if item['_id'] == account['scheduler']['_id']:
                    self._acc_coll.update_one(
                        {'_id': account_id},
                        {'$set': {'scheduler': item}}
                    )

                item['_cloner'] = account_id

            # remove all of cloned schedulers
            self._csched_coll.remove({'_id': {'$in': cloned_ids}})

            # create new cloned schedulers
            self._csched_coll.insert(real_items)

    def sync_cloned(self, cloner, id):
        '''
        Update cloned scheduler.
        If scheduler match using scheduler, update it

        :param bson.ObjectId cloner: Account identity
        :param bson.ObjectId id: Scheduler identity
        '''

        # find real scheduler
        real_item = self._sched_coll.find_one({'_id': id})
        if real_item is None:
            raise NotExistError('Not found scheduler')

        # find account
        account = self._acc_coll.find_one({'_id': cloner})
        if account is None:
            raise NotExistError('Account is not exist')

        # find cloned scheduler
        cloned_item = self._csched_coll.find_one({
            '_id': id,
            '_cloner': cloner
        })
        if cloned_item is None:
            raise NotExistError('Scheduler is not cloned')

        # padding meta data to scheduler
        real_item['_cloned_date'] = int(datetime.now().timestamp())

        # update using scheduler if match
        if 'scheduler' in account and account['scheduler']['_id'] == id:
                self._acc_coll.update_one(
                    {'_id': cloner},
                    {'$set': {'scheduler': real_item}}
                )

        # update cloned scheduler
        self._csched_coll.update_one(
            {'_id': id, '_cloner': cloner},
            {'$set': real_item}
        )

    def remove_cloned(self, acc_id, sched_id):
        '''
        Remove cloned scheduler.
        If cloned scheduler is using by account, remove it

        :param bson.ObjectId acc_id: Account identity
        :param bson.ObjectId sched_id: Scheduler identity
        '''

        # remove cloned scheduler
        res = self._csched_coll.delete_one({
            '_id': sched_id,
            '_cloner': acc_id
        })
        if res.deleted_count == 0:
            raise NotExistError('Scheduler is not exist')

        # remove using scheduler if match
        account = self._acc_coll.find_one({'_id': acc_id})
        if account is None:
            raise NotExistError('Account is not exist')
        if 'scheduler' in account and account['scheduler']['_id'] == sched_id:
            self._acc_coll.update_one(
                {'_id': acc_id},
                {'$unset': {'scheduler': None}}
            )

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
