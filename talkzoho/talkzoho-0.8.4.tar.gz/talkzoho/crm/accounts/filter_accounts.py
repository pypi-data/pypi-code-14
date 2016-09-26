from talkzoho.regions import US
from talkzoho.crm.filter_records import filter_records
from talkzoho.crm.accounts import MODULE


async def filter_accounts(*,
                          auth_token=None,
                          term=None,
                          region=US,
                          columns=None,
                          offset=0,
                          limit=None):
    return await filter_records(
        MODULE,
        auth_token=auth_token,
        term=term,
        region=region,
        columns=columns,
        offset=offset,
        limit=limit)
