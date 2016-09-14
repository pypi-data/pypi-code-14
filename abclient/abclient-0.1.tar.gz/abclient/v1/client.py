from abclient.common import http
from abclient.v1 import eisoo_backup


class Client(object):
    '''Client for the AnyBackup V1 API

    :param string endpoint : A user-supplied endpoint URL for the AB service
    '''

    def __init__(self, *arg, **kwargs):
        ''' Initialize a new client for the AnyBackup V1 API'''
        self.http_client = http._construct_http_client(*arg, **kwargs)
        self.eisoo = eisoo_backup.eisooBackupManager(self.http_client)
