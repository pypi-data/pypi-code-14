import falcon

from pyfunk import collections
from pyfunk import combinators

from pylib import lib


def error_tostring(error_map):
    """
    Converts a marshmallow validation error map to a string. The string
    follows the format "description(field)".
    @type ErrorMap => {Str: [Str]}
    @sig error_tostring :: {Str: [Str] | ErrorMap}
    """
    error_list = []
    for key, value in lib.dict_items(error_map):
        if isinstance(value, dict):
            error_list.extend(error_tostring(value))
        else:
            error_list.append('%s(%s)' % (value[0], key))
    return error_list


@combinators.curry
def top_error(many, errors):
    """
    Returns the first error from the list of validation errors
    @type ErrorMap => {Str: [Str]}
    @sig top_error :: Bool -> [ErrorMap] | ErrorMap -> Str
    """
    if many:
        # get first error in list of many
        _, entity = collections.head(lib.dict_items(errors))
        errorlist = error_tostring(entity)
        return collections.head(errorlist)
    else:
        errorlist = error_tostring(errors)
        return collections.head(errorlist)


def load(schema, obj, many=False):
    """
    Deserializes the object passed using the given schema.The object
    is validated before it is returned. If the validatation fails
    an HTTPBadRequest is raised.
    @sig load :: Schema -> {Str: a} -> Bool -> {Str: a}
    """
    data, errors = schema.load(obj, many=many)
    if bool(errors):
        err = top_error(many, errors)
        raise falcon.HTTPBadRequest('Invalid Parameters', err)
    return data


def dump(schema, obj, many=False):
    """
    Serialize the given object using the schema.
    @sig dump :: Schema -> {Str: a} -> Bool -> {Str: a}
    """
    return schema.dump(obj, many=many).data
