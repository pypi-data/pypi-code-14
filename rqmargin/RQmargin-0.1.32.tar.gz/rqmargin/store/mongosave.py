from pymongo import MongoClient


class MongoSave(object):
    def __init__(self,mongo_config):
        destination = mongo_config["destination"]
        self._mongo = MongoClient(destination, connect=False)
        self._db = self._mongo[mongo_config["database"]]

    def get_db(self):
        return self._db

    def get_client(self):
        return self._mongo