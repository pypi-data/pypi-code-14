import copy
import jsonschema

from ..lowest import scheduler


#: Model use to validate insert data
insert = copy.deepcopy(scheduler.storage)
insert['required'].remove('_id')
insert['properties'].pop('_id')

#: Model use to validate update data
update = copy.deepcopy(scheduler.storage)
update.pop('required')
update['properties'].pop('_id')
update['properties'].pop('name')


def validate_insert(items):
    '''
    Validate insert data

    :param object items: List or single data use to insert
    :raise jsonschema.exceptions.ValidationError: On data is invalid
    '''

    if type(items) is list:
        for item in items:
            jsonschema.validate(item, insert)
    else:
        jsonschema.validate(items, insert)


def validate_update(item):
    '''
    Validate update data

    :param object item: Data use to insert
    :raise jsonschema.exceptions.ValidationError: On data is invalid
    '''

    jsonschema.validate(item, update)
