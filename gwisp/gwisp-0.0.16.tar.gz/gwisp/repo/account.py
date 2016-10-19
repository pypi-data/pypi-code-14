from ..model.account import validate_insert, validate_update,\
                            validate_groups
from ..error import NotExistError, NotAllowError


verify_fields = {
    '_id': 0,
    'subject': 0,
    'name': 0,
    'groups': 0,
    'scheduler': 0,
    'schedulers': 0,
    'language': 0
}


class AccountRepo(object):
    '''
    Provide method to query account information in database

    :param pymongo.MongoClient db: Instance of connection to mongodb server
    '''
    def __init__(self, db):
        self._db = db
        self._coll = db['account']
        self._sched_coll = db['scheduler']

    def find_by_id(self, id):
        '''
        Find on account by identity

        :param bson.objectid.ObjectId id: Identity of account
        :return: Account dictionary on found
        :return: None on not found
        :rtype: dict
        '''

        return self._coll.find_one({'_id': id})

    def find_by_name(self, name):
        '''
        Find account match with name

        :param str name: Account name
        '''

        return self._coll.find_one({'name': name})

    def find_by_sub(self, sub):
        '''
        Find account match with subject

        :param str sub: Subject to find
        :return: Account directory on found
        :return: None on not found
        :rtype: dict
        '''
        return self._coll.find_one({'subject': sub})

    def insert_one(self, item):
        '''
        Insert one account into database

        :param dict item: Account dictionary
        :return: Identity of new account
        :rtype: bson.objectid.ObjectId
        '''

        if 'groups' not in item:
            item['groups'] = []
        if 'schedulers' not in item:
            item['schedulers'] = []

        validate_insert(item)

        return self._coll.insert_one(item).inserted_id

    def is_exist(self, ids):
        '''
        Verify one account is exist

        :param bson.objectid.ObjectId id: Account identity
        :return: True on account is exist
        :return: False on account is not exist
        :rtype: bool
        '''

        return self._coll.find_one({'_id': ids}, verify_fields) is not None

    def is_exist_list(self, ids):
        '''
        Verify list of account identity is exist

        :param list[bson.objectid.ObjectId] ids: List of account identity
        :return: True on all of account is exist
        :return: False on one or more account is not exist
        :rtype: bool
        '''
        cursor = self._coll.find({'_id': {'$in': ids}}, verify_fields)
        return cursor.count() == len(ids)

    def update_one(self, item):
        '''
        Update one account. Exclude name and subject fields. Item must specify
        _id field to detect what is account to update. Function only update
        fields is specify in item, other fields will be skip

        :param dict item: Account dictionary to update
        '''

        if 'email' in item:
            raise NotAllowError('Not allow update email of account')
        if 'name' in item:
            raise NotAllowError('Not allow update name of account')
        if 'subject' in item:
            raise NotAllowError('Not allow update subject of account')

        validate_update(item)
        id = item['_id']
        del item['_id']

        self._coll.update_one({'_id': id}, {'$set': item})

    def use_scheduler(self, acc_id, sched_id):
        '''
        Mark account use specify scheduler and append scheduler into
        schedulers list

        :param bson.objectid.ObjectId acc_id: Account identity which is
            use scheduler
        :param bson.objectid.ObjectId sched_id: Scheduler identity which is
            used by account
        '''

        # scheduler must be exist
        if self._sched_coll.find_one({'_id': sched_id}) is None:
            raise NotExistError('scheduler is not exist')

        # make scheduler is using
        # push scheduler to schedulers of account
        patch = {
            '$set': {'scheduler': sched_id},
            '$addToSet': {'schedulers': sched_id}
        }

        self._coll.update_one({'_id': acc_id}, patch)

    def remove_scheduler(self, acc_id, sched_id):
        '''
        Remove scheduler from schedulers list

        :param bson.objectid.ObjectId acc_id: Account identity which will
            remove scheduler
        :param bson.objectid.ObjectId sched_id: Scheduler identity will
            be remove
        '''

        patch = {
            '$pull': {'schedulers': sched_id}
        }
        self._coll.update_one({'_id': acc_id}, patch)

    def add_to_groups(self, acc_id, groups):
        '''
        Add account to groups

        :param bson.objectid.ObjectId acc_id: Account identity will be
            add to groups
        :param str group: Groups which account will be add to
        '''

        validate_groups(groups)

        patch = {
            '$addToSet': {'groups': {'$each': groups}}
        }

        self._coll.update_one({'_id': acc_id}, patch)

    def remove_from_groups(self, acc_id, groups):
        '''
        Remove account from groups

        :param bson.objectid.ObjectId acc_id: Account identity will be
            remove from groups
        :param str group: Groups which account will be remove from
        '''

        validate_groups(groups)

        patch = {
            '$pull': {'groups': {'$in': groups}}
        }

        self._coll.update_one({'_id': acc_id}, patch)
