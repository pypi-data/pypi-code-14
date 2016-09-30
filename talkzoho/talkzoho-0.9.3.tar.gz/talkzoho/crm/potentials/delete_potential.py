from talkzoho.regions import US
from talkzoho.crm.delete_record import delete_record
from talkzoho.crm.potentials import MODULE


async def delete_potential(*,
                           auth_token=None,
                           region=US,
                           id):
    return await delete_record(
        MODULE,
        auth_token=auth_token,
        region=region,
        id=id)
