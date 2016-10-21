import jsonschema

#: Account identity
attr_id = {
}

#: Password hash
attr_password_hash = {
    'type': 'string'
}

#: Created date
attr_created_date = {
    'type': 'string',
    'format': 'date-time'
}

#: Modified date
attr_modified_date = {
    'type': 'string',
    'format': 'date-time'
}

#: Schema of item use to insert
_schema_insert = {
    'type': 'object',
    'required': ['_id', 'password_hash', 'created_date'],
    'properties': {
        '_id': attr_id,
        'password_hash': attr_password_hash,
        'created_date': attr_created_date
    }
}

#: Schema of item use to update
_schema_update = {
    'type': 'object',
    'required': ['_id'],
    'properties': {
        '_id': attr_id,
        'password_hash': attr_password_hash,
        'modified_date': attr_modified_date
    }
}


def validate_insert(item):
    '''
    Validate password and meta data

    :param dict item: Password and meta data
    '''

    jsonschema.validate(item, _schema_insert)


def validate_update(item):
    '''
    Update password and meta data

    :param dict item: Password object, contains '_id' fields
    '''

    jsonschema.validate(item, _schema_update)
