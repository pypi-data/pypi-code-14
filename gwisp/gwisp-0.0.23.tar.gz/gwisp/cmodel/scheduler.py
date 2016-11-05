import jsonschema

from ..model.scheduler import attr_name, attr_tags, attr_tasks, attr_notes


_schema_post = {
    'type': 'object',
    'additionalProperties': False,
    'required': ['name', 'tags', 'tasks'],
    'properties': {
        'name': attr_name,
        'tags': attr_tags,
        'tasks': attr_tasks,
        'notes': attr_notes
    }

}

_schema_put = {
    'type': 'object',
    'additionalProperties': False,
    'properties': {
        'name': attr_name,
        'tags': attr_tags,
        'tasks': attr_tasks,
        'notes': attr_notes
    }
}


def validate_post(item):
    jsonschema.validate(item, _schema_post)


def validate_put(item):
    jsonschema.validate(item, _schema_put)
