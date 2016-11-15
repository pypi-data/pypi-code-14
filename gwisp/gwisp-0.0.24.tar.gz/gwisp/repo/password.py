from datetime import datetime
from bson.objectid import ObjectId

from ..validator import method
from ..model.lowest import password as lmodel_password
from ..model.engine import password as emodel_password


class PasswordRepo(object):
    '''
    Provide method to store password hashed and related meta data

    :param pymongo.MongoClient db: Instance of connection to mongodb server
    '''

    def __init__(self, db):
        self._db = db
        self._coll = db['password']

    @method(ObjectId, lmodel_password.attr_password_hash)
    def insert_one(self, account_id, password_hash):
        '''
        Insert one password object

        :param bson.objectid.ObjectId account_id: Account identity
            correspond with password
        :param string password_hash: Password hashed
        :raise jsonschema.exceptions.ValidationError: On input data is invalid
        '''

        password = {
            '_id': account_id,
            'password_hash': password_hash,
            'created_date': datetime.now().isoformat(),
            'modified_date': datetime.now().isoformat()
        }

        emodel_password.validate_insert(password)

        self._coll.insert_one(password)

    @method(ObjectId, lmodel_password.attr_password_hash)
    def is_exist(self, account_id, passwd_hash):
        '''
        Check pair <account identity, password> is exist

        :param bson.objectid.ObjectId account_id: Account identity
        :param str passwd_hash: Password hashed
        '''

        filters = {'_id': account_id, 'password_hash': passwd_hash}

        return self._coll.find_one(filters) is not None

    @method(ObjectId, lmodel_password.attr_password_hash)
    def update_one(self, account_id, password_hash):
        '''
        Update one password

        :param bson.objectid.ObjectId account_id: Account identity
            correspond with password
        :param string password_hash: Password hashed
        :raise jsonschema.exceptions.ValidationError: On input data is invalid
        '''

        data = {
            'password_hash': password_hash,
            'modified_date': datetime.now().isoformat()
        }

        emodel_password.validate_update(data)

        self._coll.update_one({'_id': account_id}, {'$set': data})
