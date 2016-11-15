import re
from math import ceil
from time import time
from bson import ObjectId

from .scheduler import SchedulerRepo

from ..error import NotExistError
from ..util import Selector
from ..validator import method
from ..model.engine import cscheduler as emodel_csched


search_by_author_fields = {
    'tags': 0, 'tasks': 0, 'notes': 0
}
search_by_cloner_fields = {
    'tags': 0, 'tasks': 0, 'notes': 0, '_cloner': 0
}


class CSchedulerRepo(object):
    '''
    Provide methods to manage cloned schedulers. It will help user use
    schedulers without affected from updating by author of schedulers

    :param pymongo.MongoClient db: Instance of connection to mongdb server
    '''
    def __init__(self, db):
        self._sched_repo = SchedulerRepo(db)
        self._sched_coll = db['scheduler']
        self._csched_coll = db['cscheduler']
        self._acc_coll = db['account']

    @method(ObjectId, ObjectId)
    def clone_one(self, cloner, sched_id):
        '''
        Create an cloned scheduler belong account if it is not early cloned.
        Replace data of scheduler if it is early cloned

        :param bson.objectid.ObjectId cloner: Account identity
            which is clone scheduler
        :param bson.objectid.ObjectId sched_id: Scheduler identity to clone
        '''

        # Find scheduler to clone
        real_sched = self._sched_repo.find_by_id(sched_id)
        if real_sched is None:
            raise NotExistError('Scheduler is not exist')

        # padding data
        real_sched['_cloner'] = cloner
        real_sched['_cloned_date'] = int(time())

        # validate data
        emodel_csched.validate_insert(real_sched)

        # insert or update scheduler depend on it is early exists or not
        if (self._is_exist(cloner, sched_id)):
            self._csched_coll.update_one(
                {'_id': sched_id, '_cloner': cloner},
                {'$set': real_sched}
            )
        else:
            self._csched_coll.insert_one(real_sched)

    @method(ObjectId, Selector)
    def search_on_uview(self, observer, selector=Selector()):
        '''
        Search schedulers on user view correspond with observer.
        On that view, observer see that schedulers is cloned by they or not.
        And if schedulers is cloned by they, it is updated with real schedulers
        or not.
        Two field are added to each schedulers: **_cloned** and **_updated**

        :param bson.objectid.ObjectId observer: Identity of account
        :param gwisp.Selector selector: Keyword and pagging information
        :return: List of scheduler match with selector. None on not found
        :rtype: list
        :rtype: None
        '''

        # search real schedulers
        real_items = self._sched_repo.search(selector)
        if real_items is None:
            return None

        # search cloned schedulers of account
        real_ids = [i['_id'] for i in real_items]
        cloned_cusor = self._csched_coll.find({
            '_cloner': observer,
            '_id': {'$in': real_ids}
        })
        cloned_items = list(cloned_cusor)

        # compare real and cloned schedulers to mark '_cloned' and '_updated'
        cloned_ids = [i['_id'] for i in cloned_items]
        cloned_index = {i['_id']: i for i in cloned_items}
        for item in real_items:
            # scheduler is not cloned
            if item['_id'] not in cloned_ids:
                item['_cloned'] = False
                item['_updated'] = False
                continue

            # scheduler is cloned
            item['_cloned'] = True
            cloned_item = cloned_index[item['_id']]
            if item['modified'] > cloned_item['_cloned_date']:
                item['_updated'] = False
            else:
                item['_updated'] = True

        return real_items

    @method(ObjectId, Selector)
    def search_on_cview(self, cloner, selector=Selector()):
        '''
        Search cloned schedulers on cloner view itself. On that view,
        cloner see that cloned schedulers is updated with real schedulers
        or not. One field added: '_updated'

        :param bson.objectid.ObjectId cloner: Account identity
        :param gwisp.Selector selector: Search information
        '''

        # search schedulers is cloned by account
        filters = {'$and': [{'_cloner': cloner}]}
        if selector.keyword is not None:
            filters['$and'].append(self._gen_filter(selector.keyword))

        cloned_cusor = self._csched_coll.find(
            filters,
            search_by_cloner_fields,
            skip=selector.skip,
            limit=selector.page_size
        )
        cloned_items = list(cloned_cusor)

        # search real schedulers correspond with cloned schedulers
        cloned_ids = [i['_id'] for i in cloned_items]
        real_items = self._sched_coll.find(
            {'_id': {'$in': cloned_ids}},
            {'notes': 0, 'tags': 0, 'tasks': 0, 'author': 0, 'num_user': 0}
        )

        # compare cloned schedulers with real schedulers to mar '_updated'
        real_indexs = {i['_id']: i['modified'] for i in real_items}
        for item in cloned_items:
            if real_indexs[item['_id']] > item['_cloned_date']:
                item['_updated'] = False
            else:
                item['_updated'] = True

            # remove data
            del item['_cloned_date']

        return cloned_items

    @method(ObjectId, ObjectId)
    def find_by_id_on_uview(self, observer, sched_id):
        '''
        Find one scheduler on user view correspond with observer.
        On that view, observer see that scheduler is cloned by they or not.
        And if scheduler is cloned by they, it is updated with real scheduler
        or not. Two fields are added: **_cloned** and **_updated**

        :param bson.objectid.ObjectId observer: Account identity
        :param bson.objectid.ObjectId sched_id: Scheduler identity
        :return dict: Real scheduler data on found. None on not found
        :rtype: dict
        :rtype: None
        '''

        # search real scheduler
        real_item = self._sched_repo.find_by_id(sched_id)
        if real_item is None:
            return None

        # search cloned scheduler
        cloned_item = self._csched_coll.find_one({
            '_id': sched_id,
            '_cloner': observer
        })

        # scheduler is not cloned
        if cloned_item is None:
            real_item['_cloned'] = False
            real_item['_updated'] = False
            return real_item

        # scheduler is cloned, mark '_updated' field
        real_item['_cloned'] = True
        if real_item['modified'] > cloned_item['_cloned_date']:
            real_item['_updated'] = False
        else:
            real_item['_updated'] = True

        return real_item

    @method(ObjectId, ObjectId)
    def find_by_id_on_cview(self, cloner, sched_id):
        '''
        Find cloned scheduler on cloner view itself. On that view, cloner see
        that cloned scheduler is updated with real scheduler or not.
        One field added: ‘_updated’

        :param bson.objectid.ObjectId cloner: Cloner identity
        :param bson.objectid.ObjectId sched_id: Scheduler identity
        :return: Cloned scheduler data on found. None on not found
        :rtype: dict
        :rtype: None
        '''

        # find real scheduler
        real_item = self._sched_repo.find_by_id(sched_id)
        if real_item is None:
            return None

        # find cloned scheduler
        cloned_item = self._csched_coll.find_one(
            {'_id': sched_id, '_cloner': cloner}
        )
        if cloned_item is None:
            return None

        # compare real and cloned scheduler to mark '_updated' field
        if real_item['modified'] > cloned_item['_cloned_date']:
            cloned_item['_updated'] = False
        else:
            cloned_item['_updated'] = True

        # remove data
        del cloned_item['_cloner']
        del cloned_item['_cloned_date']

        return cloned_item

    @method(ObjectId, ObjectId)
    def use_scheduler(self, account_id, sched_id):
        '''
        Make account with account_id use scheduler with sched_id.
        If scheduler is not cloned, clone it.
        Then copy cloned version to account.scheduler

        :param bson.objectid.ObjectId account_id: Account identity
        :param bson.objectid.ObjectId sched_id: Scheduler identity
        '''

        # find cloned scheduler
        cloned_item = self._csched_coll.find_one({
            '_cloner': account_id,
            '_id': sched_id
        })

        # if scheduler is not cloned, clone it
        if cloned_item is None:
            cloned_item = self._sched_repo.find_by_id(sched_id)
            if cloned_item is None:
                raise NotExistError('Scheduler is not exists')

            cloned_item['_cloner'] = account_id
            cloned_item['_cloned_date'] = int(time())

            self._csched_coll.insert_one(cloned_item)

        # copy cloned scheduler to account.scheduler
        del cloned_item['_cloner']
        self._acc_coll.update_one(
            {'_id': account_id},
            {'$set': {'scheduler': cloned_item}}
        )

    @method(ObjectId)
    def update_all_cloned(self, cloner):
        '''
        Update all of cloned schedulers is cloned by cloner with real
        schedulers

        :param bson.objectid.ObjectId cloner: Account identity
        '''

        # find schedulers is using by account
        account = self._acc_coll.find_one(
            {'_id': cloner},
            {'email': 0, 'avatar': 0, 'groups': 0, 'subject': 0}
        )
        if account is None:
            raise NotExistError('Account is not exist')

        # prepare for cloned schedulers
        number_item = self._csched_coll.count({'_cloner': cloner})
        page_size = 16
        number_of_page = ceil(number_item / page_size)

        # clone each page of schedulers
        for page_index in range(number_of_page):
            # query page of cloned schedulers
            cloned_cusor = self._csched_coll.find(
                {'_cloner': cloner},
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
                item['_cloned_date'] = int(time())

                if 'scheduler' in account:
                    if item['_id'] == account['scheduler']['_id']:
                        self._acc_coll.update_one(
                            {'_id': cloner},
                            {'$set': {'scheduler': item}}
                        )

                item['_cloner'] = cloner

            # remove all of cloned schedulers
            self._csched_coll.remove({'_id': {'$in': cloned_ids}})

            # create new cloned schedulers
            self._csched_coll.insert(real_items)

    @method(ObjectId, ObjectId)
    def update_one_cloned(self, cloner, sched_id):
        '''
        Update one cloned scheduler.
        If scheduler is using by cloner, update it

        :param bson.objectid.ObjectId cloner: Account identity
        :param bson.objectid.ObjectId sched_id: Scheduler identity
        '''

        # find real scheduler
        real_item = self._sched_coll.find_one({'_id': sched_id})
        if real_item is None:
            raise NotExistError('Not found scheduler')

        # find account
        account = self._acc_coll.find_one({'_id': cloner})
        if account is None:
            raise NotExistError('Account is not exist')

        # find cloned scheduler
        cloned_item = self._csched_coll.find_one({
            '_id': sched_id,
            '_cloner': cloner
        })
        if cloned_item is None:
            raise NotExistError('Scheduler is not cloned')

        # padding meta data to scheduler
        real_item['_cloned_date'] = int(time())

        # update using scheduler if match
        if 'scheduler' in account and account['scheduler']['_id'] == sched_id:
                self._acc_coll.update_one(
                    {'_id': cloner},
                    {'$set': {'scheduler': real_item}}
                )

        # update cloned scheduler
        self._csched_coll.update_one(
            {'_id': sched_id, '_cloner': cloner},
            {'$set': real_item}
        )

    @method(ObjectId, ObjectId)
    def remove_one_cloned(self, cloner, sched_id):
        '''
        Remove cloned scheduler from account.
        If cloned scheduler is using by account, remove it

        :param bson.objectid.ObjectId cloner: Account identity
        :param bson.objectid.ObjectId sched_id: Scheduler identity
        '''

        # remove cloned scheduler
        result = self._csched_coll.delete_one({
            '_id': sched_id,
            '_cloner': cloner
        })
        if result.deleted_count == 0:
            raise NotExistError('Scheduler is not exist')

        # remove using scheduler if match
        account = self._acc_coll.find_one({'_id': cloner})
        if account is None:
            raise NotExistError('Account is not exist')
        if 'scheduler' in account and account['scheduler']['_id'] == sched_id:
            self._acc_coll.update_one(
                {'_id': cloner},
                {'$unset': {'scheduler': None}}
            )

    @method(ObjectId, ObjectId)
    def _is_exist(self, account_id, sched_id):
        '''
        Check scheduler is cloned by account

        :param bson.objectid.ObjectId account_id: Account identity
        :param bson.objectid.ObjectId sched_id: Scheduler identity
        :return: True on scheduler is cloned by account
        :return: False on scheduelr is not cloned by account
        :rtype: bool
        '''

        key = {'account_id': account_id, '_id': sched_id}
        return self._csched_coll.find_one(key) is not None

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
