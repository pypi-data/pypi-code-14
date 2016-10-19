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

#: Notes
attr_notes = {
    'type': 'string',
    'pattern': '^(.|\n){0,1024}$'
}

#: Item use to insert
_schema_insert = {
    'required': ['name', 'author', 'tags'],
    'type': 'object',
    'properties': {
        'name': attr_name,
        'author': attr_author,
        'tags': attr_tags,
        'tasks': attr_tasks,
        'notes': attr_notes
    }
}

#: Item use to update
_schema_update = {
    'required': ['_id'],
    'type': 'object',
    'properties': {
        '_id': attr_id,
        'name': attr_name,
        'tags': attr_tags,
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
