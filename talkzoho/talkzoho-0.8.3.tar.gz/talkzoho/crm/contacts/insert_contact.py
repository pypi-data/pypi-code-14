from talkzoho.regions import US
from talkzoho.crm.insert_record import insert_record
from talkzoho.crm.contacts import MODULE


async def insert_contact(record,
                         *,
                         auth_token=None,
                         region=US):
    return await insert_record(
        MODULE,
        record=record,
        auth_token=auth_token,
        region=region)
