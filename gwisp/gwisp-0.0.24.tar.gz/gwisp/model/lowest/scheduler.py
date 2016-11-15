from .ess import object_id, account_header


#: Identity
attr_id = object_id

#: Author
attr_author = account_header

#: Name
attr_name = {
    'type': 'string',
    'pattern': '^[a-z0-9 -.]{1,64}$'
}

#: Tags
attr_tags = {
    'type': 'array',
    'items': {
        'type': 'string',
        'pattern': '^[a-z0-9]{1,16}$'
    }
}

#: Single task
attr_tasks_elem = {
    'type': 'object',
    'additionalProperties': False,
    'required': ['start', 'action'],
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

#: List of tasks
attr_tasks = {
    'type': 'array',
    'items': attr_tasks_elem
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

#: Model store in database
storage = {
    'type': 'object',
    'additionalProperties': False,
    'required': [
        '_id', 'author', 'name',
        'tags', 'num_user', 'modified',
        'tasks'
    ],
    'properties': {
        '_id': attr_id,
        'author': attr_author,
        'name': attr_name,
        'tags': attr_tags,
        'num_user': attr_num_user,
        'modified': attr_modified,
        'tasks': attr_tasks,
        'notes': attr_notes
    }
}
