from .worker import Worker
from .server import Server


class Service(object):
    '''
    This is higher public api, allow start gwisp service very quickly.
    Setup service by configuration and call ``start()`` method


    :param int port: Port which is service will be serve
    :param str db_url: Url to mongo database server
    :param str client_id: Google client identity, use for oauth-2
    :param str client_secret: Google client secret, use for oauth-2
    :param str redirect_uri: Callback url after confirm google login
    :param str jwt_key: Secret words use to sign token of service
    '''
    def __init__(self, port, db_url,
                 client_id, client_secret, redirect_uri, jwt_key):
        self._port = port
        self._db_url = db_url
        self._client_id = client_id
        self._client_secret = client_secret
        self._redirect_uri = redirect_uri
        self._jwt_key = jwt_key

    def reg_root(self, email, passwd):
        '''
        Register root account. Name is gwisp

        :param str email: Email of root account
        :param str passwd: Password in text plain
        '''

        worker = self._gen_worker()
        worker.reg_root(email, passwd)

        worker.stop()

    def start(self):
        '''
        Use gunicorn as server to create worker and serve
        '''

        self._server = Server(
            self._port, self._db_url, self._client_id, self._client_secret,
            self._redirect_uri, self._jwt_key
        )
        self._server.run()

    def renew_db(self):
        '''
        Ensure database have correct index and empty data
        '''

        worker = self._gen_worker()
        worker.renew_db()

        worker.stop()

    def setup(self, asset_dir):
        '''
        Drop database if it is exist. Create new database with correct
        indexs. Install sample data

        :param str asset_dir: Path to asset directory.
            See :ref:`api_asset_dir`
        '''

        worker = self._gen_worker()
        worker.setup(asset_dir)

        worker.stop()

    def _gen_worker(self):
        return Worker(
            self._db_url,
            self._client_id, self._client_secret, self._redirect_uri,
            self._jwt_key
        )
