from datetime import datetime

from ..model.password import validate_insert, validate_update
from ..error import NotAllowError


class PasswordRepo(object):
    '''
    Password repository
    Use to store password hashed and meta data related with password

    :param pymongo.MongoClient db: Instance of connection to mongodb server
    '''

    def __init__(self, db):
        self._db = db
        self._coll = db['password']

    def is_exist(self, id, passwd_hash):
        '''
        Check pair identity-password is exist

        :param bson.objectid.ObjectId id: Identity of account
        :param str password: Password
        '''

        filters = {'_id': id, 'password_hash': passwd_hash}

        return self._coll.find_one(filters) is not None

    def insert_one(self, item):
        '''
        Insert one password object

        :param dict item: Password hashed and meta data
        '''

        if 'created_date' in item:
            raise NotAllowError('created_date is auto fill')
        if 'modified_date' in item:
            raise NotAllowError('modified_date is auto fill')

        item['created_date'] = datetime.now().isoformat()
        item['modified_date'] = datetime.now().isoformat()

        validate_insert(item)

        self._coll.insert_one(item)

    def update_one(self, item):
        '''
        Update password

        :param dict item: New password hashed
        '''

        if 'created_date' in item:
            raise NotAllowError('created_date is not allowed to update')
        if 'modified_date' in item:
            raise NotAllowError('modified_date is auto fill')

        item['modified_date'] = datetime.now().isoformat()

        validate_update(item)

        id = item['_id']
        del item['_id']

        self._coll.update_one({'_id': id}, {'$set': item})
