import copy
import jsonschema

from ..lowest import account


#: Model use to validate insert data
insert = copy.deepcopy(account.storage)
insert['required'].remove('_id')
insert['required'].remove('scheduler')
insert['properties'].pop('_id')


#: Model use to validate update data
update = copy.deepcopy(account.storage)
update.pop('required')
update['properties'].pop('_id')
update['properties'].pop('name')
update['properties'].pop('email')
update['properties'].pop('subject')


def validate_insert(item):
    '''
    Validate insert data

    :param dict item: Data use to insert account
    :raise jsonschema.exceptions.ValidationError: On data is invalid
    '''

    jsonschema.validate(item, insert)


def validate_update(item):
    '''
    Validate update data

    :param dict: Data use to update account
    :raise jsonschema.exceptions.ValidationError: On data is invalid
    '''

    jsonschema.validate(item, update)
