
import os
import json
import uuid
import requests
from porper.controllers.auth_controller import AuthController

class GithubAuthController(AuthController):

    def __init__(self, permission_connection):

        AuthController.__init__(self, permission_connection)

        self.auth_endpoint = os.environ.get('GITHUB_AUTH_ENDPOINT')
        self.api_endpoint = os.environ.get('GITHUB_API_ENDPOINT')
        self.client_id = os.environ.get('GITHUB_CLIENT_ID')
        self.client_secret = os.environ.get('GITHUB_CLIENT_SECRET')

        if not self.auth_endpoint:
            with open('config.json') as data_file:
                config = json.load(data_file)
            #print config
            self.auth_endpoint = config['github']['auth_endpoint']
            self.api_endpoint = config['github']['api_endpoint']
            self.client_id = config['github']['client_id']
            self.client_secret = config['github']['client_secret']

    def authenticate(self, code, state, redirect_uri):

        print "code [%s], state [%s], redirect_uri [%s]" % (code, state, redirect_uri)

        # first find the access token from the given code & state
        access_token_url = "%s/access_token" % (self.auth_endpoint)
        post_data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": code,
            "redirect_uri": redirect_uri,
            "state": state
        }
        headers = {"Content-Type":"application/json"}
        r = requests.post(access_token_url, headers=headers, data=json.dumps(post_data), verify=False)
        print r
        print r._content
        """
        access_token=f378a5dd8da8422472d1875011db11ea9ccbd9c8&scope=&token_type=bearer
        """
        try:
            access_token = r._content.split('&')[0].split('=')[1]
        except Exception:
            raise Exception("unauthorized")

        # now find the user info from the access token
        user_url = "%s/user?access_token=%s"%(self.api_endpoint, access_token)
        r = requests.get(user_url, verify=False)
        print r._content
        """
        {
            "login": "",
            "id": 0000,
            "avatar_url": "https://avatars.githubusercontent.com/u/....",
            "gravatar_id": "",
            "url": "https://api.github.com/users/....",
            "html_url": "https://github.com/....",
            "followers_url": "https://api.github.com/users/....",
            "following_url": "https://api.github.com/users/....",
            "gists_url": "https://api.github.com/users/....",
            "starred_url": "https://api.github.com/users/....",
            "subscriptions_url": "https://api.github.com/users/....",
            "organizations_url": "https://api.github.com/users/....",
            "repos_url": "https://api.github.com/users/....",
            "events_url": "https://api.github.com/users/....",
            "received_events_url": "https://api.github.com/users/....",
            "type": "User",
            "site_admin": false,
            "name": "  ",
            "company": null,
            "blog": null,
            "location": null,
            "email": "   ",
            "hireable": null,
            "bio": null,
            "public_repos": 11,
            "public_gists": 0,
            "followers": 4,
            "following": 0,
            "created_at": "2008-11-21T23:30:05Z",
            "updated_at": "2016-06-22T12:48:31Z"
        }
        """
        user_info = json.loads(r._content)

        # now save the user info & tokens
        AuthController.authenticate(self,
            str(user_info['id']),
            user_info['email'],
            "",
            "",
            user_info['name'],
            access_token,
            code)

        # return the access_token if all completed successfully
        user_info['user_id'] = user_info['id']
        user_info['access_token'] = access_token
        user_info['roles'] = AuthController.find_roles(self, user_info['email'])
        return user_info
