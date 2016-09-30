
import os
import json
import uuid
import requests
from porper.controllers.auth_controller import AuthController

class GoogleAuthController(AuthController):

    def __init__(self, permission_connection):

        AuthController.__init__(self, permission_connection)

        self.tokeninfo_endpoint = os.environ.get('GOOGLE_TOKENINFO_ENDPOINT')

        if not self.tokeninfo_endpoint:
            with open('config.json') as data_file:
                google_info = json.load(data_file)
            #print google_info
            self.tokeninfo_endpoint = google_info['google']['tokeninfo_endpoint']

    def authenticate(self, id_token):

        # get the tokens to see if the given code is valid
        print "id_token [%s]" % id_token
        url = "%s%s"%(self.tokeninfo_endpoint, id_token)
        r = requests.get(url, verify=False)
        print r._content
        """{
            "iss": "accounts.google.com",
            "at_hash": "",
            "aud": "",
            "sub": "",
            "email_verified": "true",
            "azp": "",
            "email": "",
            "iat": "1466089125",
            "exp": "1466092725",
            "name": "",
            "picture": "",
            "given_name": "",
            "family_name": "",
            "locale": "en",
            "alg": "RS256",
            "kid": ""
        }"""
        user_info = json.loads(r._content)
        if not user_info.get('email_verified'):
            raise Exception("unauthorized")

        # now save the user info & tokens
        access_token = str(uuid.uuid4())
        AuthController.authenticate(self,
            user_info['sub'],
            user_info['email'],
            user_info['family_name'],
            user_info['given_name'],
            user_info['name'],
            access_token,
            id_token)

        # return the access_token if all completed successfully
        user_info['user_id'] = user_info['sub']
        user_info['access_token'] = access_token
        user_info['roles'] = AuthController.find_roles(self, user_info['email'])
        return user_info
