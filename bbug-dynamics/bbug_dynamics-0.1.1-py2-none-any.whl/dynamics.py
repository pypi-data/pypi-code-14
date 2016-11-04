import adal, httplib, urllib, json, boto3
from io import StringIO

class Dynamics:
    def __init__(self,settings):
        self.bbug_company_id = settings['Item']['bbug_company_id']
        self.settings = settings['Item']['dynamics']
        self._token= self.token()
        self.dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        self.messages = []

    def query(self, params={}):
        params = urllib.urlencode(params)
        if params!='' :
            params = '?' + params

        headers = { 'Authorization': 'Bearer ' + self._token['accessToken'],
                   'Content-Type': 'application/json; charset=utf-8',
                   'Accept': 'application/json',
                   'OData-Version': 4.0
                  }
        conn= httplib.HTTPSConnection(self.settings['web_api_resource'])
        request_uri = self.settings['canonical_api_uri'] + self.base_uri() + params
        conn.request('GET',request_uri,'', headers )
        self.response= conn.getresponse()

    def base_uri(self):
        return '/'

    def process_response(self):
        if self.response.status == 200:
            d = self.response.read()
            data=json.loads(d)
            return data['value']
        else:
            raise "Cannot get dynamics entities"

    def token(self):
        authority_url = ('https://login.microsoftonline.com/' +
                        self.settings['tenant'])

        RESOURCE = 'https://' + self.settings['web_api_resource']

        context = adal.AuthenticationContext(authority_url)

        token = context.acquire_token_with_username_password(
            RESOURCE,
            self.settings['user'],
            self.settings['password'],
            self.settings['client_id'])
        return token

