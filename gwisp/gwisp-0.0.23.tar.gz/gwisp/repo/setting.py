from ..model.setting import validate_insert
from ..error import NotAllowError


class SettingRepo(object):
    '''
    Setting Repository

    :param pymongo.MongoClient db: Instance connection to mongo server
    '''

    def __init__(self, db):
        self._db = db
        self._coll = db['setting']

    def insert_one(self, item):
        '''
        Insert one setting into database

        :pram dict item: Setting item
        '''

        validate_insert(item)

        if not self.is_empty():
            raise NotAllowError('Allow only item in collection')

        self._coll.insert_one(item)

    def is_empty(self):
        '''
        Check collection is empty

        :return: True on empty, False on otherwise
        :rtype: bool
        '''

        return self._coll.find_one() is None
