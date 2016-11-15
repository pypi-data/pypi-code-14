import jsonschema

from ..lowest import password as password_lmodel


def validate_insert(account_id, password_hash):
    '''
    Validate data use to insert

    :param bson.ObjectId account_id: Account identity corresponding with
        password
    :param string password_hash: Password after hash
    :raise jsonschema.exceptions.ValidationError: On data is invalid
    '''

    jsonschema.validate(account_id, password_lmodel.attr_id)
    jsonschema.validate(password_hash, password_lmodel.attr_password_hash)


def validate_update(account_id, password_hash):
    '''
    Validate data use to update

    :param bson.ObjectId account_id: Account identity corresponding with
        password
    :param string password_hash: Password after hash
    :raise jsonschema.exceptions.ValidationError: On data is invalid
    '''

    jsonschema.validate(account_id, password_lmodel.attr_id)
    jsonschema.validate(password_hash, password_lmodel.attr_password_hash)
