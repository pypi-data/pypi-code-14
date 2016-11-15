import jsonschema

from ..lowest import rtoken as rtoken_lmodel


def validate_insert(account_id):
    '''
    Validate data use to insert

    :param bson.ObjectId account_id: Account identity corresponding
        with refresh token
    :raise jsonschema.exceptions.ValidationError: On data is invalid
    '''

    jsonschema.validate(account_id, rtoken_lmodel.attr_account_id)
