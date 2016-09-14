from abclient.common import http
from abclient.v1 import eisoo_backup


class Client(object):
    '''Client for the AnyBackup V1 API

    :param string endpoint : A user-supplied endpoint URL for the AB service.
    :param string machine_code : A user-supplied AnyBackup client code for the
        AB service identify backup clients.
    '''

    def __init__(self, endpoint, machine_code, **kwargs):
        ''' Initialize a new client for the AnyBackup V1 API'''
        self.http_client = http._construct_http_client(endpoint, **kwargs)
        self.eisoo = eisoo_backup.eisooBackupManager(self.http_client,
                                                     machine_code, **kwargs)
