import os

from urllib.parse import urlencode

from tornado.httpclient import AsyncHTTPClient
from tornado.escape import json_decode

from talkzoho.utils import create_url
from talkzoho.regions import US
from talkzoho.projects import BASE_URL, API_PATH, ENVIRON_AUTH_TOKEN
from talkzoho.projects.utils import unwrap_items


async def get_record(*,
                     id,
                     module,
                     portal_id,
                     auth_token=None,
                     region=US,
                     columns=None):
    query = urlencode({
        'authtoken': auth_token or os.getenv(ENVIRON_AUTH_TOKEN)})

    client   = AsyncHTTPClient()
    path     = API_PATH + '/portal/' + portal_id + '/' + module + '/' + id + '/'
    endpoint = create_url(BASE_URL, tld=region, path=path)

    url      = endpoint + '?' + query
    response = await client.fetch(url, method='GET')
    body     = json_decode(response.body.decode("utf-8"))

    return unwrap_items(body, single_item=True, columns=columns)
