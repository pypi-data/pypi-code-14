import os
from math import ceil

from urllib.parse import urlencode

from fuzzywuzzy import fuzz

from tornado.httpclient import AsyncHTTPClient
from tornado.httpclient import HTTPError as HTTPClientError
from tornado.web import HTTPError
from tornado.escape import json_decode

from talkzoho.regions import US
from talkzoho.utils import create_url

from talkzoho.books import BASE_URL, API_PATH, SCOPE, MAX_PAGE_SIZE, ENVIRON_AUTH_TOKEN


async def filter_module(module,
                        *,
                        auth_token=None,
                        organization_id=None,
                        term=None,
                        region=US,
                        columns=None,
                        offset=0,
                        limit=None):
    client   = AsyncHTTPClient()
    path     = API_PATH + '/' + module
    endpoint = create_url(BASE_URL, tld=region, path=path)

    if limit == 0:
        return []
    elif not term and limit and limit <= MAX_PAGE_SIZE:
        batch_size = limit
    else:
        batch_size = MAX_PAGE_SIZE

    paging     = True
    page_index = max(ceil(offset / batch_size), 1)
    results    = []

    # Loop until we reach index we need, unless their is a search term.
    # If search term we need all records.
    while paging and (term or not limit or len(results) < limit):
        url = endpoint + '?' + urlencode({
            'scope': SCOPE,
            'authtoken': auth_token or os.getenv(ENVIRON_AUTH_TOKEN),
            'organization_id': organization_id,
            'per_page': batch_size,
            'page': page_index})

        try:
            response = await client.fetch(url, method='GET')
        except HTTPClientError as http_error:
            http_code = http_error.code
            response  = json_decode(http_error.response.body.decode("utf-8"))
            message   = str(response['code']) + ': ' + response['message']
            raise HTTPError(http_code, reason=message)
        else:
            response    = json_decode(response.body.decode("utf-8"))
            results    += response[module]
            page_index += 1
            paging      = response['page_context']['has_more_page']

    def fuzzy_score(price_list):
        values = [str(v).lower() for v in price_list.values() if v]
        target = ' '.join(values)
        return fuzz.partial_ratio(term, target)

    if term:
        results = sorted(results, key=fuzzy_score, reverse=True)

    results = results[:limit]
    if columns:
        return [{k: pl[k] for k in columns if k in columns} for pl in results]
    else:
        return results
