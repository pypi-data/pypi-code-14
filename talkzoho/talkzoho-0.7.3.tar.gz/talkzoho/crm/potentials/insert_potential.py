from talkzoho.regions import US
from talkzoho.crm.insert_module import insert_module
from talkzoho.crm.potentials import MODULE, PRIMARY_FIELD


async def insert_potential(record,
                           *,
                           auth_token=None,
                           region=US):
    return await insert_module(
        MODULE,
        primary_field=PRIMARY_FIELD,
        record=record,
        auth_token=auth_token,
        region=region)
