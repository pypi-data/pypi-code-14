import os

from typing import Optional, Union

from urllib.parse import urlencode

from tornado.httpclient import AsyncHTTPClient
from tornado.escape import json_decode

from talkzoho import logger
from talkzoho.regions import US
from talkzoho.utils import create_url

from talkzoho.crm import BASE_URL, API_PATH, SCOPE, ENVIRON_AUTH_TOKEN
from talkzoho.crm.utils import select_columns, unwrap_items


async def get_record(module: str,
                     *,
                     auth_token: Optional[str]=None,
                     region: str=US,
                     columns: Optional[list]=None,
                     id: Union[int, str]):
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

    url = endpoint + '?' + urlencode(query)

    logger.info('GET: {}'.format(url))
    response = await client.fetch(url, method='GET')
    body     = json_decode(response.body.decode('utf-8'))

    return unwrap_items(body, single_item=True)
