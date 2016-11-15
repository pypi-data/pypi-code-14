import copy
import jsonschema

from ..lowest import password


#: Model use to validate insert data
insert = copy.deepcopy(password.storage)

#: Model use to validate update data
update = copy.deepcopy(password.storage)
update['required'].remove('_id')
update['required'].remove('created_date')
update['properties'].pop('_id')
update['properties'].pop('created_date')


def validate_insert(item):
    '''
    Validate insert data

    :param dict: Data use to insert
    :raise jsonschema.exceptions.ValidationError: On data is invalid
    '''

    jsonschema.validate(item, insert)


def validate_update(item):
    '''
    Validate update data

    :param dict: Data use to update
    :raise jsonschema.exceptions.ValidationError: On data is invalid
    '''

    jsonschema.validate(item, update)
