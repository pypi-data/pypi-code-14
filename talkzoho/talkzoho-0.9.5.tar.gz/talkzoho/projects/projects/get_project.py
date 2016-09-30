from talkzoho.regions import US
from talkzoho.projects.get_record import get_record

from talkzoho.projects.projects import MODULE


async def get_project(*,
                      id,
                      portal_id,
                      auth_token=None,
                      region=US,
                      columns=None):
    return await get_record(
        id=id,
        module=MODULE,
        portal_id=portal_id,
        auth_token=auth_token,
        region=region,
        columns=columns)
