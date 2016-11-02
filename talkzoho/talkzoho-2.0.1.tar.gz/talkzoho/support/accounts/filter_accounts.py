import os

from urllib.parse import urlencode

from fuzzywuzzy import fuzz

from tornado.httpclient import AsyncHTTPClient
from tornado.escape import json_decode
from tornado.web import HTTPError

from talkzoho.utils import create_url
from talkzoho.regions import US
from talkzoho.support.utils import select_columns, unwrap_items
from talkzoho.support import \
    BASE_URL, API_PATH, ENVIRON_AUTH_TOKEN, MAX_PAGE_SIZE
from talkzoho.support.accounts import MODULE


async def filter_accounts(*,
                          auth_token=None,
                          term=None,
                          region=US,
                          columns=None,
                          offset=0,
                          limit=None,
                          portal,
                          department):
    client   = AsyncHTTPClient()
    path     = API_PATH + '/' + MODULE + '/getrecords'
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
            'department': department,
            'fromindex': from_index,
            'toindex': to_index,
            'portal': portal}

        if columns:
            query['selectfields'] = select_columns(MODULE, columns)

        url      = endpoint + '?' + urlencode(query)
        response = await client.fetch(url, method='GET')
        body     = json_decode(response.body.decode("utf-8"))

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
