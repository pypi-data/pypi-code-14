from datetime import datetime, timedelta
from bson.objectid import ObjectId

from ..validator import method
from ..model.lowest import rtoken as lmodel_rtoken
from ..model.engine import rtoken as emodel_rtoken


class RtokenRepo(object):
    '''
    Provide methods to manage refresh token

    :param pymongo.MongoClien db: Instance of connection to mongdb server
    '''

    def __init__(self, db):
        self._db = db
        self._coll = db['rtoken']

    @method(lmodel_rtoken.attr_id, ObjectId, timedelta)
    def insert_one(self, rtoken_id, account_id, expires_in=timedelta(days=30)):
        '''
        Insert a refresh token

        :param string rtoken_id: Refresh token identity
        :param bson.objectid.ObjectId account_id: Account identity which is
            own refresh token
        :param string expires_in: Time span from now specify expired of refresh
            token
        '''

        expired_date = (datetime.now() + expires_in).timestamp()

        rtoken = {
            '_id': rtoken_id,
            'account_id': account_id,
            'expired': int(expired_date)
        }

        emodel_rtoken.validate_insert(rtoken)

        self._coll.insert_one(rtoken)

    @method(lmodel_rtoken.attr_id)
    def verify_and_remove(self, rtoken_id):
        '''
        Find refresh token in storage.
        If exist, get refresh token, verify and remove from storage.
        If refresh token is valid, return refresh toke, else return None

        :param str rtoken_id: Refresh token identity
        :return: Refresh token data
        :rtype: dict
        :rtype: None
        '''

        rtoken = self._coll.find_one({'_id': rtoken_id})
        if rtoken is None:
            return None

        self._coll.delete_one({'_id': rtoken_id})

        now = datetime.now().timestamp()
        if rtoken['expired'] < now:
            return None

        return rtoken
