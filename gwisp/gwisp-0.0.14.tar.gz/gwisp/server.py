from gunicorn.app.base import BaseApplication

from .worker import Worker


class Server(BaseApplication):
    '''
    Use gunicorn to make server. It will be create worker, auto restart
    after worker terminate

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

        super(Server, self).__init__()

    def load_config(self):
        '''
        Override method of BaseApplication of gunicorn
        '''

        if self._port > 0:
            self.cfg.set('bind', '0.0.0.0:{}'.format(self._port))

    def load(self):
        '''
        Override method of BaseApplication of gunicorn
        '''

        worker = Worker(self._db_url,
                        self._client_id, self._client_secret,
                        self._redirect_uri, self._jwt_key)
        return worker.start()
