from talkzoho.regions import US
from talkzoho.crm.get_record import get_record
from talkzoho.crm.potentials import MODULE


async def get_potential(*,
                       auth_token=None,
                       region=US,
                       columns=None,
                       id):
    return await get_record(
        MODULE,
        auth_token=auth_token,
        region=region,
        columns=columns,
        id=id)
