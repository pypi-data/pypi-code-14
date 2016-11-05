import jsonschema

#: Identity
attr_id = {
    'type': 'string',
    'pattern': '^[a-zA-Z0-9]{22}$'
}

#: Account identity
attr_account_id = {
}

#: Expired
attr_expired = {
    'type': 'integer'
}

#: Item use to insert
_schema_insert = {
    'type': 'object',
    'required': ['_id', 'account_id', 'expired'],
    'properties': {
        '_id': attr_id,
        'account_id': attr_account_id,
        'expired': attr_expired
    }
}


def validate_insert(item):
    '''
    Validate refresh token will be create

    :param object item: Refresh token object
    '''

    jsonschema.validate(item, _schema_insert)
