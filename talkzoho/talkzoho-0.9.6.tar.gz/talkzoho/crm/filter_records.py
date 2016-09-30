import os

from typing import Optional

from urllib.parse import urlencode

from fuzzywuzzy import fuzz

from tornado.httpclient import AsyncHTTPClient
from tornado.web import HTTPError
from tornado.escape import json_decode

from talkzoho import logger
from talkzoho.regions import US
from talkzoho.utils import create_url

from talkzoho.crm import BASE_URL, API_PATH, SCOPE, MAX_PAGE_SIZE, ENVIRON_AUTH_TOKEN
from talkzoho.crm.utils import select_columns, unwrap_items


async def filter_records(module: str,
                         *,
                         auth_token: Optional[str]=None,
                         term: Optional[str]=None,
                         region: str=US,
                         columns: Optional[list]=None,
                         offset: int=0,
                         limit: Optional[int]=None):
    client   = AsyncHTTPClient()
    path     = API_PATH + '/' + module + '/getRecords'
    endpoint = create_url(BASE_URL, tld=region, path=path)

    if limit == 0:
        return []
    elif not term and limit and limit <= MAX_PAGE_SIZE:
        batch_size = limit
    else:
        batch_size = MAX_PAGE_SIZE

    paging     = True
    from_index = offset + 1  # Zoho indexes at one not zero
    to_index   = offset + batch_size
    results    = []

    # Loop until we reach index we need, unless their is a search term.
    # If search term we need all records.
    while paging and (term or limit is None or to_index <= limit):
        query = {
            'authtoken': auth_token or os.getenv(ENVIRON_AUTH_TOKEN),
            'fromIndex': from_index,
            'toIndex': to_index,
            'newFormat': 2,
            'version': 2,
            'scope': SCOPE}

        if columns:
            query['selectColumns'] = select_columns(module, columns)

        url = endpoint + '?' + urlencode(query)

        logger.info('GET: {}'.format(url))
        response = await client.fetch(url, method='GET')
        body     = json_decode(response.body.decode('utf-8'))

        try:
            items = unwrap_items(body)
        except HTTPError as http_error:
            # if paging and hit end suppress error
            # unless first request caused the 404
            if http_error.status_code == 404 and from_index - 1 != offset:
                paging = False
            else:
                raise
        else:
            results   += items
            from_index = to_index + 1
            to_index  += batch_size

    def fuzzy_score(resource):
        values = [str(v) for v in resource.values() if v]
        target = ' '.join(values)
        return fuzz.partial_ratio(term, target)

    if term:
        results = sorted(results, key=fuzzy_score, reverse=True)

    return results[:limit]
