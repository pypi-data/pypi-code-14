import jsonschema
from .scheduler import attr_id as sched_id, attr_name as sched_name,\
                       attr_tags as sched_tags, attr_tasks as sched_tasks,\
                       attr_notes as sched_notes


#: Identify
attr_id = {

}

#: Email
attr_email = {
    'type': 'string',
    'pattern': '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
}

#: Name
attr_name = {
    'type': 'string',
    'pattern': '^[a-z0-9 -.]{1,64}$'
}

#: Subject
attr_subject = {
    'type': 'string'
}

#: Groups
attr_groups = {
    'type': 'array',
    'items': {
        'type': 'string',
        'pattern': '^[a-z0-9]{1,8}$'
    }
}

#: Scheduler
attr_scheduler = {
    'type': 'object',
    'properties': {
        '_id': sched_id,
        'name': sched_name,
        'tags': sched_tags,
        'tasks': sched_tasks,
        'notes': sched_notes
    }
}

#: Schedulers
attr_schedulers = {
    'type': 'array',
    'items': sched_id
}

#: Language
attr_language = {
    'type': 'string',
    'pattern': '^[a-z]{2}$'
}

#: Item use to insert
_schema_insert = {
    'type': 'object',
    'required': ['email', 'name', 'subject', 'language'],
    'properties': {
        'email': attr_email,
        'name': attr_name,
        'subject': attr_subject,
        'groups': attr_groups,
        'scheduler': attr_scheduler,
        'schedulers': attr_schedulers,
        'language': attr_language
    }
}

#: Item use to update
_schema_update = {
    'type': 'object',
    'required': ['_id'],
    'properties': {
        '_id': attr_id,
        'groups': attr_groups,
        'scheduler': attr_scheduler,
        'schedulers': attr_schedulers,
        'language': attr_language
    }
}


def validate_insert(item):
    '''
    Validate account will be create

    :param object item: Account object
    '''

    jsonschema.validate(item, _schema_insert)


def validate_update(item):
    '''
    Validate account will be update

    :param object item: Account object
    '''

    jsonschema.validate(item, _schema_update)


def validate_groups(groups):
    '''
    Validate groups of account

    :param object item: Account object
    '''

    jsonschema.validate(groups, attr_groups)
