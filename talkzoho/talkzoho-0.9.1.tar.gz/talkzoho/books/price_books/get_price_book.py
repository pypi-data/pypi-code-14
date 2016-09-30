import os

from urllib.parse import urlencode

from tornado.httpclient import AsyncHTTPClient
from tornado.httpclient import HTTPError as HTTPClientError
from tornado.web import HTTPError
from tornado.escape import json_decode

from talkzoho.regions import US
from talkzoho.utils import create_url

from talkzoho.books import BASE_URL, API_PATH, SCOPE, ENVIRON_AUTH_TOKEN

RESOURCE = 'pricebooks'


async def get_price_book(*,
                         auth_token=None,
                         region=US,
                         columns=None,
                         organization_id,
                         id):
    client   = AsyncHTTPClient()
    path     = API_PATH + '/' + RESOURCE + '/' + str(id)
    endpoint = create_url(BASE_URL, tld=region, path=path)
    url      = endpoint + '?' + urlencode({
        'organization_id': organization_id,
        'authtoken': auth_token or os.getenv(ENVIRON_AUTH_TOKEN)})

    try:
        response = await client.fetch(url, method='GET')
    except HTTPClientError as http_error:
        http_code = http_error.code
        response  = json_decode(http_error.response.body.decode("utf-8"))
        message   = str(response['code']) + ': ' + response['message']
        raise HTTPError(http_code, reason=message)
    else:
        response = json_decode(response.body.decode("utf-8"))
        results  = [v for k, v in response.items() if k not in ['code', 'message']]

        if len(results) != 1:
            ValueError('More then one resource was returned.')

        return results[0]
