import pkg_resources

from ..repo import AccountRepo, SchedulerRepo


class RootCtl(object):
    '''
    Information of service. Read only resource
    '''

    def __init__(self, db):
        '''
        :param pymongo.MongoClient db: Instance of connection to mongodb server
        '''

        self._acc_repo = AccountRepo(db)
        self._sched_repo = SchedulerRepo(db)

    def on_get(self, req, res):
        '''
        Response: Essential information of service
        '''

        data = {
            'name': 'gwisp service',
            'notes': 'programing interface of scheduler storage on http',
            'version': pkg_resources.get_distribution('gwisp').version,
            'source': 'https://github.com/kevin-leptons/gwisp',
            'doc': 'http://gwisp.readthedocs.io/en/latest/',
            'num_user': self._acc_repo.count(),
            'num_sched': self._sched_repo.count()
        }

        res.body = data
