import os

from urllib.parse import urlencode

from fuzzywuzzy import fuzz

from tornado.httpclient import AsyncHTTPClient
from tornado.escape import json_decode
from tornado.web import HTTPError

from talkzoho.utils import create_url
from talkzoho.regions import US
from talkzoho.projects import BASE_URL, API_PATH, ENVIRON_AUTH_TOKEN, MAX_PAGE_SIZE  # noqa
from talkzoho.projects.utils import unwrap_items


async def filter_projects(*,
                          auth_token=None,
                          term=None,
                          region=US,
                          columns=None,
                          offset=0,
                          limit=None,
                          portal_id):
    client   = AsyncHTTPClient()
    path     = API_PATH + '/portal/' + portal_id + '/projects/'
    endpoint = create_url(BASE_URL, tld=region, path=path)

    if limit == 0:
        return []
    elif not term and limit and limit <= MAX_PAGE_SIZE:
        batch_size = limit
    else:
        batch_size = MAX_PAGE_SIZE

    paging     = True
    from_index = offset
    to_index   = offset + batch_size - 1
    results    = []

    # Loop until we reach index we need, unless their is a search term.
    # If search term we need all records.
    while paging:
        query = urlencode({
            'authtoken': auth_token or os.getenv(ENVIRON_AUTH_TOKEN),
            'index': from_index + 1,  # Zoho indexes at one not zero,
            'range': batch_size})

        url           = endpoint + '?' + query
        response      = await client.fetch(url, method='GET')
        reached_limit = limit and to_index + 1 >= limit

        if response.code == 204 or (term is None and reached_limit):
            break

        body  = json_decode(response.body.decode("utf-8"))
        items = unwrap_items(body, columns=columns)

        results   += items
        from_index = to_index + 1
        to_index  += batch_size

    def fuzzy_score(resource):
        values = [str(v).lower() for v in resource.values() if v]
        target = ' '.join(values)
        return fuzz.partial_ratio(term, target)

    if term:
        results = sorted(results, key=fuzzy_score, reverse=True)

    return results[:limit]
