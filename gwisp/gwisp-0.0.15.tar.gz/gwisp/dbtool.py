import json
import glob
from os import path
from gwisp.repo import SchedulerRepo, AccountRepo


class DbTool(object):
    '''
    Controll install sample data into database

    :param pymongo.MongoClient db: Instance of connection to mongodb server
    :param str asset_dir: Path to static asset directory. That's directory
        must contains file specifications. See :ref:`api_asset_dir`
    '''
    def __init__(self, db, asset_dir, account):
        self._db = db                   #: Instance of mongodb client
        self._asset_dir = asset_dir     #: Path to asset directory

        self._sched_repo = SchedulerRepo(db)    #: Scheduler repository
        self._acc_repo = AccountRepo(db)        #: Account repository

        #: Real account identity
        self._account = account
        self._acc_id = self._acc_repo.insert_one(account)

    def install(self):
        '''
        Install sample data into database

        :return: Number of data files has been readed
        :rtype: int
        '''

        return self.install_scheduler()

    def install_scheduler(self):
        '''
        Install sample scheduler into database

        :return: Number of data files has been readed
        :rtype: int
        '''

        files = glob.glob(path.join(self._asset_dir, 'scheduler-*.json'))
        items = []
        nfiles = 0

        for file in files:
            nfiles += 1

            with open(file) as f:
                item = json.load(f)
                item['author'] = self._acc_id
                items.append(item)

            if len(items) == 128:
                self._sched_repo.insert_many(items)
                items = []

        if len(items) > 0:
                self._sched_repo.insert_many(items)

        return nfiles
