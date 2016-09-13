import os

from urllib.parse import urlencode

from tornado.httpclient import AsyncHTTPClient
from tornado.escape import json_decode

from talkzoho.regions import US
from talkzoho.utils import create_url

from talkzoho.crm import BASE_URL, API_PATH, SCOPE, ENVIRON_AUTH_TOKEN
from talkzoho.crm.utils import select_columns, unwrap_items


async def get_module(module,
                     *,
                     auth_token=None,
                     region=US,
                     columns=None,
                     id):
    client   = AsyncHTTPClient()
    path     = API_PATH + '/' + module + '/getRecordById'
    endpoint = create_url(BASE_URL, tld=region, path=path)
    query    = {
        'id': id,
        'scope': SCOPE,
        'version': 2,
        'newFormat': 2,
        'authtoken': auth_token or os.getenv(ENVIRON_AUTH_TOKEN)}

    if columns:
        query['selectColumns'] = select_columns(module, columns)

    url      = endpoint + '?' + urlencode(query)
    response = await client.fetch(url, method='GET')
    body     = json_decode(response.body.decode("utf-8"))

    return unwrap_items(body, single_item=True)
