import jsonschema
import copy

from .scheduler import _schema_insert as scheduler_insert, attr_id


#: Account identity who is used scheduler
attr_cloner = {
}

#: Cloned date
attr_cloned_date = {
    'type': 'integer'
}

#: Schema of item to insert
_schema_insert = copy.deepcopy(scheduler_insert)
_schema_insert['required'].extend(['_id', '_cloner', '_cloned_date'])
_schema_insert['properties'].update({
    '_id': attr_id,
    '_cloner': attr_cloner,
    '_cloned_date': attr_cloned_date
})


def validate_insert(item):
    '''
    Validate item to insert

    :param dict item: Cloned scheduler
    '''

    jsonschema.validate(item, _schema_insert)
