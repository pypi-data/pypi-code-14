import copy
import jsonschema

from ..lowest import cscheduler

#: Model use to validate insert data
insert = copy.deepcopy(cscheduler.storage)


def validate_insert(item):
    '''
    Validate insert data

    :param dict item: Data use to insert
    :raise jsonschema.exceptions.ValidationError: On data is invalid
    '''

    jsonschema.validate(item, insert)
