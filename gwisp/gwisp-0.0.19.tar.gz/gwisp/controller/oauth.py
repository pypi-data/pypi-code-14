from ..error import AuthenticateError


class BasicLoginCtl(object):
    '''
    Login by username and password

    :param gwisp.Protector protector: Instance of protector
    '''

    def __init__(self, protector):
        self._protector = protector

    def on_get(self, req, res):
        '''
        Request: Username and password in header

        Response: Token string
        '''

        if 'USERNAME' not in req.headers.keys():
            raise AuthenticateError('Username header is not set')
        if 'PASSWORD' not in req.headers.keys():
            raise AuthenticateError('Passowrd header is not set')

        token = self._protector.login_by_passwd(
            req.headers['USERNAME'],
            req.headers['PASSWORD']
        )

        res.body = {
            'access_token': token
        }


class LoginUrlCtl(object):
    '''
    Information about how to login

    :param gwisp.Protector protector: Instance of protector
    '''

    def __init__(self, protector):
        self._protector = protector

    def on_get(self, req, res):
        '''
        Response: Login url
        '''

        res.body = {
            'url': self._protector.login_url
        }


class LoginCtl(object):
    '''
    Support login by google oauth-2

    :param gwisp.Protector protector: Instance of protector
    '''

    def __init__(self, protector):
        self._protector = protector

    def on_get(self, req, res):
        '''
        Request: Login code from google as query param

        Response: Token string
        '''

        access_token = self._protector.login_by_code(req.params['code'])
        res.body = {
            'access_token': access_token
        }


class MeCtl(object):
    '''
    Account information

    :param pymongo.MongoClient db: Instance of mongo client
    :param gwisp.Protector protector: Instance of protector
    '''

    def __init__(self, db, protector):
        self._db = db
        self._protector = protector

    def on_get(self, req, res):
        '''
        Request: Token in header

        Response: Account information
        '''

        info = self._protector.check(req, True)
        res.body = info.account
