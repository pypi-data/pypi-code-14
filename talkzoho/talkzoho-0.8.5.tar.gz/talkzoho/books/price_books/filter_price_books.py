from talkzoho.regions import US

from talkzoho.books.filter_module import filter_module

RESOURCE = 'pricebooks'


async def filter_price_books(*,
                             auth_token=None,
                             organization_id=None,
                             term=None,
                             region=US,
                             columns=None,
                             offset=0,
                             limit=None):
    return await filter_module(
        RESOURCE,
        auth_token=auth_token,
        organization_id=organization_id,
        term=term,
        region=region,
        columns=columns,
        offset=offset,
        limit=limit)
