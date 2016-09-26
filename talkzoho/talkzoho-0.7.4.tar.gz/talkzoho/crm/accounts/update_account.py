from talkzoho.regions import US
from talkzoho.crm.update_module import update_module
from talkzoho.crm.accounts import MODULE, PRIMARY_FIELD


async def update_account(record,
                         *,
                         auth_token=None,
                         region=US):
    return await update_module(
        MODULE,
        primary_field=PRIMARY_FIELD,
        record=record,
        auth_token=auth_token,
        region=region)
