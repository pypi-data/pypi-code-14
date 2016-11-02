import os

from urllib.parse import urlencode

from fuzzywuzzy import fuzz

from tornado.httpclient import AsyncHTTPClient
from tornado.web import HTTPError
from tornado.escape import json_decode

from talkzoho.regions import US
from talkzoho.utils import create_url

from talkzoho.support import BASE_URL, API_PATH, ENVIRON_AUTH_TOKEN
from talkzoho.support.utils import select_columns, unwrap_items
from talkzoho.support.accounts import MODULE


async def get_account(*,
                      auth_token=None,
                      region=US,
                      columns=None,
                      portal,
                      department,
                      id):
    client   = AsyncHTTPClient()
    path     = API_PATH + '/' + MODULE + '/getrecordsbyid'
    endpoint = create_url(BASE_URL, tld=region, path=path)
    query    = {
        'id': id,
        'authtoken': auth_token or os.getenv(ENVIRON_AUTH_TOKEN),
        'portal': portal,
        'department': department}

    if columns:
        query['selectfields'] = select_columns(MODULE, columns)

    url      = endpoint + '?' + urlencode(query)
    print(url)
    response = await client.fetch(url, method='GET')
    body     = json_decode(response.body.decode("utf-8"))

    return unwrap_items(body, single_item=True)
