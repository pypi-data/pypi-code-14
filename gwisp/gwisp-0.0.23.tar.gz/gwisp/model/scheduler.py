import jsonschema


#: Identify
attr_id = {
}

#: Name
attr_name = {
    'type': 'string',
    'pattern': '^[a-z0-9 -.]{1,64}$'
}

#: Author
attr_author = {
    'type': 'object',
    'required': ['_id', 'name'],
    'additionalProperties': False,
    'properties': {
        '_id': {
            'type': 'string',
            'pattern': '^[a-fA-F0-9]{24}$'
        },
        'name': {
            'type': 'string',
            'pattern': '^[a-z0-9 -.]{1,64}$'
        }
    }
}

#: Tags
attr_tags = {
    'type': 'array',
    'items': {
        'type': 'string',
        'pattern': '^[a-z0-9]{1,16}$'
    }
}

#: Tasks
attr_tasks = {
    'type': 'array',
    'items': {
        'type': 'object',
        'required': ['start', 'action'],
        'additionalProperties': False,
        'properties': {
            'start': {
                'type': 'string',
                'pattern': '^([0-1][0-9]|2[0-3]):[0-5][0-9]$'
            },
            'action': {
                'type': 'string',
                'pattern': '^[a-zA-Z0-9 ]{1,32}$'
            }
        }
    }
}

#: Number of user cloned scheduler
attr_num_user = {
    'type': 'integer'
}

#: Last modified date
attr_modified = {
    'type': 'integer'
}

#: Notes
attr_notes = {
    'type': 'string',
    'pattern': '^(.|\n){0,1024}$'
}

#: Item use to insert
_schema_insert = {
    'type': 'object',
    'additionalProperties': False,
    'required': ['name', 'author', 'tags', 'num_user', 'modified'],
    'properties': {
        'name': attr_name,
        'author': attr_author,
        'tags': attr_tags,
        'num_user': attr_num_user,
        'modified': attr_modified,
        'tasks': attr_tasks,
        'notes': attr_notes
    }
}

#: Item use to update
_schema_update = {
    'required': ['_id', 'modified'],
    'type': 'object',
    'additionalProperties': False,
    'properties': {
        '_id': attr_id,
        'tags': attr_tags,
        'num_user': attr_num_user,
        'modified': attr_modified,
        'tasks': attr_tasks,
        'notes': attr_notes
    }
}


def validate_insert(items):
    '''
    Validate scheduler use to insert

    :param object items: List or single of schedulers
    '''

    if type(items) is list:
        for item in items:
            jsonschema.validate(item, _schema_insert)
    else:
        jsonschema.validate(items, _schema_insert)


def validate_update(items):
    '''
    Validate scheduler to update

    :param object items: List or single of schedulers
    '''

    if type(items) is list:
        for item in items:
            jsonschema.validate(items, _schema_update)
    else:
        jsonschema.validate(items, _schema_update)
