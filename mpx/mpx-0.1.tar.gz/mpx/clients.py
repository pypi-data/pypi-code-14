#!/usr/bin/env python


from .exceptions import *

AUTH_URL = 'https://identity.auth.theplatform.{tld}/idm'
MEDIA_URL = 'http://data.media.theplatform.{tld}/media'

class HttpClient(object):
    def call(self,
                method,
                url,
                path,
                headers={},
                **kwargs
            ):
        print(self)
        try:
            response = requests.get( url, params=params, headers=headers )
            data = json.loads( response.text )
        except Exception as e:
            raise GenericError( str(e) )

        return data


class AuthClient(object):
    def __init__(self, 
                    username,
                    password,
                    accounts=[],
                    region='US1',
                    token_duration=60000,
                    cache_token=True,
                ):
        print( locals() )
        self.username = username
        self.password = password
        self.accounts = accounts
        self.region = region
        self.token_duration = token_duration
        self.cache_token = cache_token

    def get_url(self, url):
        print( locals() )
        tld = 'eu' if 'eu' in self.region.lower() else 'com'
        return url.format(tld = tld)


class GenericClient(object):
    def __init__(self, base_url, path, auth_client ):
        print( locals() )
        self.base_url = base_url
        self.path = path
        self.auth_client = auth_client

