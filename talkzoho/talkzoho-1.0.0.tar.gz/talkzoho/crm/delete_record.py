import os

from typing import Optional, Union

from urllib.parse import urlencode

from tornado.httpclient import AsyncHTTPClient
from tornado.escape import json_decode

from talkzoho import logger
from talkzoho.regions import US
from talkzoho.utils import create_url

from talkzoho.crm import BASE_URL, API_PATH, SCOPE, ENVIRON_AUTH_TOKEN
from talkzoho.crm.utils import unwrap_items


async def delete_record(module: str,
                        *,
                        auth_token: Optional[str]=None,
                        region: str=US,
                        id: Union[int, str]):
    client   = AsyncHTTPClient()
    path     = API_PATH + '/' + module + '/deleteRecords'
    endpoint = create_url(BASE_URL, tld=region, path=path)
    query    = {
        'id': id,
        'scope': SCOPE,
        'authtoken': auth_token or os.getenv(ENVIRON_AUTH_TOKEN)}

    url = endpoint + '?' + urlencode(query)

    logger.info('DELETE: {}'.format(url))
    response = await client.fetch(url, method='GET')
    body     = json_decode(response.body.decode('utf-8'))

    return unwrap_items(body, single_item=True)
