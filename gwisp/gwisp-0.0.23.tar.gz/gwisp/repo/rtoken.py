import random
from datetime import datetime, timedelta
from string import ascii_lowercase, ascii_uppercase, digits

from ..model.rtoken import validate_insert


class RtokenRepo(object):
    '''
    Provide methods to manage refresh token

    :param pymongo.MongoClien db: Instance of connection to mongdb server
    '''

    def __init__(self, db):
        self._db = db
        self._coll = db['rtoken']

    def create_one(self, account_id):
        '''
        Generate a refresh token and insert to storage

        :param dict item: Refresh token dictionary
        :rerturn: Refresh token
        :rtype: dict
        '''

        rtoken_chars = ascii_uppercase + ascii_lowercase + digits
        rtoken_len = 22
        id = ''.join(random.choice(rtoken_chars) for i in range(rtoken_len))
        expired_date = (datetime.now() + timedelta(days=30)).timestamp()

        item = {
            '_id': id,
            'account_id': account_id,
            'expired': int(expired_date)
        }

        validate_insert(item)

        self._coll.insert_one(item)

        return item

    def verify_and_remove(self, id):
        '''
        Find refresh token in storage.
        If exist, get refresh token, verify and remove from storage.
        If refresh token is valid, return refresh token.
        Else, return None

        :param str id: Refresh token identity
        :return: Refresh token
        :rtype: dict
        :rtype: None
        '''

        item = self._coll.find_one({'_id': id})
        if item is None:
            return None

        self._coll.delete_one({'_id': id})

        now = datetime.now().timestamp()
        if item['expired'] < now:
            return None

        return item
