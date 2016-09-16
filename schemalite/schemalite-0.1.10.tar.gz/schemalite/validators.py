from .schema_error import SchemaError
from .core import func_and_desc

def type_validator(*types):
    def validator(o, data):
        if not any(isinstance(o, _type) for _type in types):
            raise SchemaError('TypeError')
    return validator


def type_list_validator(*types):
    def validator(olist, data):
        valid = True
        errors = []
        for o in olist:
            if any(isinstance(o, _type) for _type in types):
                valid = valid & True
                errors.append(None)
            else:
                valid = False
                errors.append('TypeError')
        if not valid:
            raise SchemaError(errors)
    return validator


def chained_validator(*validators):
    def validator(o, data):
        for _validator in validators:
            if _validator is None:
                continue
            _validator(o, data)

    return validator


def is_a_type_of(*types):
    def validator(o, data):
        if not any(isinstance(o, _type) for _type in types):
            return (False, 'TypeError')
        return (True, None)
    return func_and_desc(
        validator,
        "Should be of type {0}".format("/".join([_t.__name__ for _t in types])))


def is_a_list_of_types_of(*types):
    def validator(olist, data):
        valid = True
        errors = []
        for o in olist:
            if any(isinstance(o, _type) for _type in types):
                valid = valid & True
                errors.append(None)
            else:
                valid = False
                errors.append('TypeError')
        return (valid, errors)
    return func_and_desc(
        validator,
        "Should be a list of objects of type {0}".format("/".join([_t.__name__ for _t in types])))
