import httplib2
import hashlib

import jwt
import datetime
from bson.objectid import ObjectId
from oauth2client.client import OAuth2WebServerFlow
from apiclient import discovery

from .error import AuthenticateError, AuthorizeError
from .repo import PasswordRepo, AccountRepo
from .util import AuthInfo


class Protector(object):
    '''
    Control authenticating and authorizing

    :param pymongo.MongoClient db: Instance of connection to mongo server
    :param string client_id: Google oauth-2 client identify
    :param string client_secret: Google oauth-2 client secret
    :param list scope: Google oauth-2 scope
    :param string redirect_uri: Oauth-2 callback uri
    :param string jwt_key: Secret word use to sign token
    '''
    def __init__(self, db, client_id, client_secret, scope, redirect_uri,
                 jwt_key):
        self._db = db
        self._client_id = client_id
        self._client_secret = client_secret
        self._scope = scope
        self._redirect_uri = redirect_uri
        self._jwt_key = jwt_key

        self._acc_repo = AccountRepo(db)
        self._passwd_repo = PasswordRepo(db)

    def create_account(self, account, password):
        '''
        Create an account with password

        :param dict account: Account information
        :param str password: Password to login
        '''

        acc_id = self._acc_repo.insert_one(account)

        passwd_hash = hashlib.sha224(password.encode('utf-8')).hexdigest()
        passwd = {
            '_id': acc_id,
            'password_hash': passwd_hash
        }

        self._passwd_repo.insert_one(passwd)

    @property
    def login_url(self):
        '''
        Get oauth-2 login url. Use browser and url to login by google oauth-2
        service

        :return: Url use to login
        :rtype: str
        '''

        oauth = self._gen_oauth2()
        return oauth.step1_get_authorize_url()

    def login_by_passwd(self, name, password):
        '''
        Login by account name and password

        :param str name: Name of account
        :param str password: Password
        :return: Token string
        :rtype: str
        '''

        account = self._acc_repo.find_by_name(name)
        if account is None:
            raise AuthenticateError('Account is not exist')

        passwd_hash = hashlib.sha224(password.encode('utf-8')).hexdigest()
        match = self._passwd_repo.is_exist(account['_id'], passwd_hash)
        if match is False:
            raise AuthenticateError('Password is incorrect')

        return self._gen_token(account['_id'])

    def login_by_code(self, code):
        '''
        Login by code from google. If google account has not early login,
        create an account

        :param str code: Code what is received from google oauth-2 service
        :return: Token what is to authenticate and authorize
        :rtype: string
        '''

        # exchange code to tokens
        oauth = self._gen_oauth2()
        credentials = oauth.step2_exchange(code)

        # use token to get google account information
        http = credentials.authorize(httplib2.Http())
        service = discovery.build('plus', 'v1')
        req = service.people().get(userId='me')
        me = req.execute(http=http)

        # verify google account is early register in system
        # if not, register first
        sub = credentials.id_token['sub']
        acc = self._acc_repo.find_by_sub(sub)
        if acc is None:
            acc = {
                'subject': sub,
                'email': credentials.id_token['email'],
                'name': me['displayName'],
                'language': me['language'],
                'avatar': me['image']['url']
            }
            self._acc_repo.insert_one(acc)

        # system token
        return self._gen_token(acc['_id'])

    def check(self, req, iacc=False, group=None):
        '''
        Authenticate and authorize if **group** parameter is specify

        :param falcon.Request req: Contains information about http request
        :param boolean iacc: Decide include account information
        :param string group: Group what is expected account in
        :return: Information after authenticate and authorize
        :rtype: gwisp.AuthInfo
        '''

        token = self.authenticate(req.headers['AUTHORIZATION'])
        acc_id = ObjectId(token['sub'])
        acc = None

        if iacc is True:
            acc = self._acc_repo.find_by_id(acc_id)
            if acc is None:
                raise AuthenticateError('Can not identity user')

        if group is not None:
            if iacc is False:
                acc = self._acc_repo.find_by_id(acc_id)
            if acc is None:
                raise AuthenticateError('Can no identity user')
            if group not in acc['group']:
                raise AuthorizeError('Invalid permission')

        return AuthInfo(acc_id, token, acc)

    def authenticate(self, token):
        '''
        Identify account by decode token

        :param string token: Token to decode
        :return: Token has decoded
        :rtype: dict
        '''

        return jwt.decode(token, self._jwt_key)

    def _gen_oauth2(self):
        '''
        Create an oauth-2 web server flow object

        :return: Instance of OAuth2WebServerFlow
        :rtype: oauth2client.client.OAuth2WebServerFlow
        '''

        return OAuth2WebServerFlow(
            client_id=self._client_id,
            client_secret=self._client_secret,
            scope=self._scope,
            redirect_uri=self._redirect_uri)

    def _gen_token(self, acc_id):
        '''
        Create token string

        :param bson.objectid.ObjectId acc_id: Identity of account
        :return: Token string
        :rtype: str
        '''

        token_data = {
            'sub': str(acc_id),
            'exp': datetime.datetime.now().timestamp() + 3600
        }
        token = jwt.encode(token_data,
                           self._jwt_key,
                           algorithm='HS512')

        return token.decode()
