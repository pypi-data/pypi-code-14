import jsonschema

#: Root account
attr_root_name = {
    'type': 'string',
    'regex': '^[a-zA-Z0-9 -.]{1,64}$'
}

#: Installed date
attr_date = {
    'type': 'string',
    'format': 'date-time'
}

#: Internet address installed
attr_ip = {
    'type': 'string',
    'format': 'ipv4',
}

#: Item to insert
_schema_insert = {
    'type': 'object',
    'required': ['root_name', 'date', 'ip'],
    'properties': {
        'root_name': attr_root_name,
        'date': attr_date,
        'ip': attr_ip
    }
}


def validate_insert(item):
    '''
    Validate setting to insert

    :param dict item: Item to validate
    '''

    jsonschema.validate(item, _schema_insert)
