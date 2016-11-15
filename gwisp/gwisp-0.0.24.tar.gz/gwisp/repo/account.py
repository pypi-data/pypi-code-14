from bson.objectid import ObjectId

from ..error import NotExistError
from ..validator import method
from ..model.repo import account as rmodel_account
from ..model.engine import account as emodel_account
from ..model.lowest import account as lmodel_account


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
        self._coll = db['account']
        self._sched_coll = db['scheduler']

    @method(rmodel_account.insert)
    def insert_one(self, data):
        '''
        Insert one account into database

        :param dict data: Account data
        :return: Identity of new account
        :rtype: bson.objectid.ObjectId
        :raise jsonschema.exceptions.ValidationError: On input data is invalid
        '''

        # padding data
        if 'groups' not in data:
            data['groups'] = []

        emodel_account.validate_insert(data)

        return self._coll.insert_one(data).inserted_id

    @method(ObjectId)
    def find_by_id(self, id):
        '''
        Find one account by identity

        :param bson.objectid.ObjectId id: Identity of account
        :return: Account data on found
        :return: None on not found
        :rtype: dict
        '''

        return self._coll.find_one({'_id': id})

    @method(str)
    def find_by_name(self, name):
        '''
        Find one account by name

        :param str name: Account name
        :return: Account data on found
        :return: None on not found
        :rtype: dict
        '''

        return self._coll.find_one({'name': name})

    @method(str)
    def find_by_sub(self, sub):
        '''
        Find account by subject. Subject is identity of goole account

        :param str sub: Subject to find
        :return: Account data on found
        :return: None on not found
        :rtype: dict
        '''
        return self._coll.find_one({'subject': sub})

    @method(ObjectId)
    def is_exist(self, id):
        '''
        Verify one account identity is exist

        :param bson.objectid.ObjectId id: Account identity
        :return: True on account is exist
        :return: False on account is not exist
        :rtype: bool
        '''

        return self._coll.find_one({'_id': id}, verify_fields) is not None

    @method(ObjectId, rmodel_account.update)
    def update_one(self, id, data):
        '''
        Update one account

        :param bson.objectid.ObjectId id: Account identity
        :param dict data: Data use to update
        :raise jsonschema.exceptions.ValidationError: On input data is invalid
        '''

        result = self._coll.update_one({'_id': id}, {'$set': data})

        if result.matched_count == 0:
            raise NotExistError('Account is not exists to update')

    @method(ObjectId, lmodel_account.attr_groups)
    def add_to_groups(self, acc_id, groups):
        '''
        Add account to groups. If group is early exists, do nothing

        :param bson.objectid.ObjectId acc_id: Account identity will be
            add to groups
        :param list groups: List of groups add to account
        :raise jsonschema.exceptions.ValidationError: On input data is invalid
        '''

        patch = {
            '$addToSet': {'groups': {'$each': groups}}
        }

        self._coll.update_one({'_id': acc_id}, patch)

    @method(ObjectId, lmodel_account.attr_groups)
    def remove_from_groups(self, acc_id, groups):
        '''
        Remove account from groups. If group is not exists,  do nothing

        :param bson.objectid.ObjectId acc_id: Account identity will be
            remove from groups
        :param list groups: Groups which account will be remove from
        :raise jsonschema.exceptions.ValidationError: On input data is invalid
        '''

        patch = {
            '$pull': {'groups': {'$in': groups}}
        }

        self._coll.update_one({'_id': acc_id}, patch)

    def count(self):
        '''
        Count number of accounts in collection

        :return: Number of accounts
        :rtype: int
        '''

        return self._coll.count()
