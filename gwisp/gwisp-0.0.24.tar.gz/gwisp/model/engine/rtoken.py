import copy
import jsonschema

from ..lowest import rtoken


#: Model use to validate insert data
insert = copy.deepcopy(rtoken.storage)


def validate_insert(item):
    '''
    Validate insert data

    :param dict: Data use to insert
    :raise jsonschema.exceptions.ValidationError: On data is invalid
    '''

    jsonschema.validate(item, insert)
