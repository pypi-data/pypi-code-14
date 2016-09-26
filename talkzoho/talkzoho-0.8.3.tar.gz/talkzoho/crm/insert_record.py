import os

from typing import Union, Optional

from urllib.parse import urlencode

from tornado.httpclient import AsyncHTTPClient
from tornado.escape import json_decode

from talkzoho.regions import US
from talkzoho.utils import create_url

from talkzoho.crm import BASE_URL, API_PATH, SCOPE, ENVIRON_AUTH_TOKEN
from talkzoho.crm.utils import wrap_items, unwrap_items


async def insert_record(module: str,
                        record: dict,
                        *,
                        auth_token: Optional[str]=None,
                        region: str=US,
                        trigger_workflow: bool=True):
    client     = AsyncHTTPClient()
    path       = API_PATH + '/' + module + '/insertRecords'
    endpoint   = create_url(BASE_URL, tld=region, path=path)
    xml_record = wrap_items(record, module_name=module)

    query = {
        'scope': SCOPE,
        'version': 2,
        'newFormat': 2,
        'duplicateCheck': 1,
        'wfTrigger': str(trigger_workflow).lower(),
        'xmlData': xml_record,
        'authtoken': auth_token or os.getenv(ENVIRON_AUTH_TOKEN)}

    url      = endpoint + '?' + urlencode(query)
    response = await client.fetch(url, method='POST', allow_nonstandard_methods=True)  # noqa
    body     = json_decode(response.body.decode('utf-8'))

    if type(record) is list:
        results = unwrap_items(body, single_item=False)
        return [r['Id'] for r in results]
    else:
        return unwrap_items(body, single_item=True)['Id']
