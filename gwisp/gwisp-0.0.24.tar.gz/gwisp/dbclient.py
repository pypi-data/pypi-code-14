from os import path
from pymongo import MongoClient
from .collection import specs
from .error import CollectionIndexError


class DbClient(object):
    '''
    Provide general action of mongodb. And guaranteed that make a database
    with correct indexs

    :param str url: Url to mongodb server, include username and password
    '''
    def __init__(self, url):
        self._url = url
        self._dbname = path.basename(self._url)

    @property
    def db(self):
        '''
        :return: Instance of connection to mongodb
        :rtype: pymongo.MongoClient
        '''

        return self._db

    def connect(self):
        '''
        Connect to mongodb server
        '''

        self._mongo_client = MongoClient(self._url)
        self._db = self._mongo_client[self._dbname]

    def close(self):
        '''
        Close connection to mongodb server
        '''

        self._mongo_client.close()
        self._mongo_client = None

    def drop(self):
        '''
        Drop current database
        '''

        self._mongo_client.drop_database(self._dbname)
        self._mongo_client = None

    def check_indexs(self):
        '''
        Check indexs of database

        :raise CollectionIndexError: Indexes of collection is invalid
        '''

        # check for each collection has defined
        for spec in specs:
            db_indexes = self._db[spec.name].index_information()

            # check for each index of collection has defined
            for index_name in spec.indexes:
                if index_name not in db_indexes:
                    raise CollectionIndexError(spec.name)
                db_index = db_indexes[index_name]

                if spec.indexes[index_name]['key'] != db_index['key']:
                    raise CollectionIndexError(spec.name)
                if spec.indexes[index_name]['unique'] != db_index['unique']:
                    raise CollectionIndexError(spec.name)

    def renew(self):
        '''
        If database is early exist then drop it
        Create new database with empty collections
        '''

        self.drop()
        self.connect()

        for spec in specs:
            self._db.create_collection(spec.name)
            coll = self._db[spec.name]

            for index_name in spec.indexes.keys():
                coll.create_index(
                    spec.indexes[index_name]['key'],
                    name=index_name,
                    unique=spec.indexes[index_name]['unique']
                )

    def is_empty(self):
        '''
        Check database is empty or not

        :returns: True on database is empty
        :returns: False on database is not empty
        :rtype: bool
        '''

        return len(self._db.collection_names()) == 0
