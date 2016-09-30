import os

from urllib.parse import urlencode

from tornado.httpclient import AsyncHTTPClient
from tornado.escape import json_decode

from talkzoho import logger
from talkzoho.regions import US
from talkzoho.utils import create_url

from talkzoho.crm import BASE_URL, API_PATH, SCOPE, ENVIRON_AUTH_TOKEN
from talkzoho.crm.utils import wrap_items, unwrap_items


async def upload_file(module: str,
                      *,
                      auth_token: str=None,
                      region: str=US,
                      id: str,
                      url: str):
    client     = AsyncHTTPClient()
    path       = API_PATH + '/' + module + '/uploadFile'
    endpoint   = create_url(BASE_URL, tld=region, path=path)

    body = urlencode({
        'id': id,
        'scope': SCOPE,
        'attachmentUrl': url,
        'authtoken': auth_token or os.getenv(ENVIRON_AUTH_TOKEN)})

    logger.info('POST: {}, BODY: {}'.format(endpoint, body))
    response = await client.fetch(endpoint, method='POST', body=body)
    body     = json_decode(response.body.decode('utf-8'))

    return unwrap_items(body, single_item=True)['Id']
