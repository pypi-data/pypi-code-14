from falcon import HTTPBadRequest, HTTP_204

from ..error import AuthenticateError
from ..repo import AccountRepo


class OauthCtl(object):

    '''
    Implement oauth-2 endpoint by essential supported

    :param gwisp.protector protector: Instance of protector
    '''

    def __init__(self, protector):
        self._protector = protector

    def on_post(self, req, res):
        params = req.context['body']

        if 'grant_type' not in params:
            raise HTTPBadRequest(
                title='400 Bad Request',
                description='Not support grant_type'
            )

        if params['grant_type'] == 'password':
            self._grant_passwd(req, res)
        elif params['grant_type'] == 'refresh_token':
            self._grant_rtoken(req, res)
        else:
            raise HTTPBadRequest(
                title='400 Bad Request',
                description='Not support grant_type'
            )

    def _grant_passwd(self, req, res):
        params = req.context['body']

        if 'username' not in params:
            raise AuthenticateError('Username is not set')
        if 'password' not in params:
            raise AuthenticateError('Passowrd is not set')

        res.body = self._protector.login_by_passwd(
            params['username'],
            params['password']
        )

    def _grant_rtoken(self, req, res):
        params = req.context['body']

        if 'refresh_token' not in params:
            raise AuthenticateError('Refresh token is not set')

        res.body = self._protector.refresh_token(params['refresh_token'])


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

        res.body = self._protector.login_by_code(req.params['code'])


class MeCtl(object):
    '''
    Account information

    :param pymongo.MongoClient db: Instance of mongo client
    :param gwisp.Protector protector: Instance of protector
    '''

    def __init__(self, db, protector):
        self._protector = protector
        self._acc_repo = AccountRepo(db)

    def on_get(self, req, res):
        '''
        Request: Token in header

        Response: Account information
        '''

        info = self._protector.check(req, True)
        del info.account['subject']
        res.body = info.account

    def on_put(self, req, res):
        '''
        Request: Token in header and content in body

        Response: No Content
        '''

        auth = self._protector.check(req)

        self._acc_repo.update_one(auth.account_id, req.context['body'])

        res.status = HTTP_204
