import copy
import jsonschema

from ..lowest import account as account_lmodel
from ..engine import account as account_emodel


#: Model use to validate insert
insert = copy.deepcopy(account_emodel.insert)

#: Model use to validate update
update = copy.deepcopy(account_emodel.update)


def validate_insert(item):
    '''
    Validate data use to insert

    :param dict item: Data use to insert
    :raise jsonschema.exceptions.ValidationError: On data is invalid
    '''

    jsonschema.validate(item, insert)


def validate_update(item):
    '''
    Validate data use to update

    :param dict item: Data use to update
    :raise jsonschema.exceptions.ValidationError: On data is invalid
    '''

    jsonschema.validate(item, update)


def validate_groups(data):
    '''
    Validate groups of account

    :param list data: Groups of account
    :raise jsonschema.exceptions.ValidationError: On data is invalid
    '''

    jsonschema.validate(data, account_lmodel.attr_groups)
