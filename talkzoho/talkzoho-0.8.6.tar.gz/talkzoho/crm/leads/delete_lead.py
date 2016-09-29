from talkzoho.regions import US
from talkzoho.crm.delete_record import delete_record
from talkzoho.crm.leads import MODULE


async def delete_lead(*,
                      auth_token=None,
                      region=US,
                      id):
    return await delete_record(
        MODULE,
        auth_token=auth_token,
        region=region,
        id=id)
